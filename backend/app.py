from flask import Flask, render_template,jsonify, send_file
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from celery.schedules import crontab
import os
import csv
from datetime import datetime,timedelta
from weasyprint import HTML
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from models import init_db, Influencer, Sponsor, Campaign, Advertisement, Request, Feedback
from extensions import cache
from resources.sponsor import SponsorSignUp, SponsorLogin, SponsorProfile, SponsorUpdateProfile
from resources.influencer import InfluencerSignUp, InfluencerLogin, InfluencerProfile, InfluencerUpdateProfile
from resources.campaign import CampaignAPI, SponsorFlaggedCampaignsAPI
from resources.advertisement import AdvertisementAPI, InfluencerAdsAPI
from resources.request import RequestAPI, RequestActionAPI, SponsorRequestToInfluencerAPI, InfluencerNegotiationAPI
from resources.admin import AdminLogin, OngoingCampaigns, FlaggedItems, FlagItem, UnflagItem, Statistics, AllUsers
from resources.feedback import FeedbackResource, AverageRatingResource


app = Flask(__name__, static_folder='static', static_url_path='/static')
api = Api(app)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'Akhil'
app.config['SECRET_KEY'] = 'Akhil'
app.config['DEBUG'] = True

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(current_dir, "database.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "no-reply@sponsorsphere.com"
SENDER_PASSWORD = ""

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/1",
        result_backend="redis://localhost:6379/2",
        enable_utc=False,
        timezone="Asia/Kolkata",
        broker_connection_retry_on_startup=True
    ),
)

celery_app = Celery(app.name)
celery_app.config_from_object(app.config["CELERY"])

class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask

init_db(app)

api.add_resource(SponsorSignUp, '/sponsor/signup')
api.add_resource(SponsorLogin, '/sponsor/signin')
api.add_resource(SponsorProfile, '/sponsor/profile') 
api.add_resource(SponsorUpdateProfile, '/sponsor/profile/update') 
api.add_resource(InfluencerSignUp, '/influencer/signup')
api.add_resource(InfluencerLogin, '/influencer/login')
api.add_resource(InfluencerProfile, '/influencer/profile') 
api.add_resource(InfluencerUpdateProfile, '/influencer/profile/update') 
api.add_resource(CampaignAPI, '/campaign/<int:CampaignID>', '/campaign') 
api.add_resource(AdvertisementAPI, '/advertisement', '/advertisement/<int:AdvertisementID>', '/campaign/<int:CampaignID>/ads')
api.add_resource(InfluencerAdsAPI, '/influencer/ads') 
api.add_resource(RequestAPI, '/requests')
api.add_resource(RequestActionAPI, '/requests/<int:request_id>/<string:action>')
api.add_resource(SponsorRequestToInfluencerAPI, '/requests/sponsor/to_influencer/<int:influencer_id>')
api.add_resource(AdminLogin, '/admin/login')
api.add_resource(InfluencerNegotiationAPI, '/requests/negotiate/<int:request_id>')
api.add_resource(FeedbackResource, '/feedback', '/feedback/<int:influencer_id>')
api.add_resource(AverageRatingResource, '/average-rating/<int:influencer_id>')
api.add_resource(OngoingCampaigns, '/admin/ongoing-campaigns')
api.add_resource(FlaggedItems, '/admin/flagged-items')
api.add_resource(FlagItem, '/admin/flag/<string:item_type>/<int:item_id>')
api.add_resource(UnflagItem, '/admin/unflag/<string:item_type>/<int:item_id>')
api.add_resource(Statistics, '/admin/statistics')
api.add_resource(SponsorFlaggedCampaignsAPI, '/sponsor/flagged-campaigns')
api.add_resource(AllUsers, '/admin/all-users')

#Celery endpoints

@app.route('/test-celery', methods=['GET'])
def test_celery_endpoint():
    task = test_task.delay()
    return jsonify({"message": "Celery test task triggered", "task_id": task.id}), 202

@app.route('/trigger-daily-reminders', methods=['GET'])
def trigger_daily_reminders_endpoint():
    task = send_daily_reminders.delay()
    return jsonify({"message": "Daily reminders task triggered", "task_id": task.id}), 202

@app.route('/trigger-monthly-report', methods=['GET'])
def trigger_monthly_report_endpoint():
    task = send_monthly_activity_report.delay()
    return jsonify({"message": "Monthly activity report task triggered", "task_id": task.id}), 202

@app.route('/export-campaign-csv/<int:campaign_id>', methods=['GET'])
def export_campaign_csv_endpoint(campaign_id):
    file_path = generate_campaign_details_as_csv(campaign_id) 
    if not file_path:
        return jsonify({"msg": "Campaign not found"}), 404

    return send_file(file_path, as_attachment=True, download_name=f'campaign_{campaign_id}.csv', mimetype='text/csv')

def generate_campaign_details_as_csv(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return None  
    
    campaign_data = {
        "CampaignID": campaign.CampaignID,
        "Title": campaign.Title,
        "Description": campaign.Description,
        "Budget": campaign.Budget,
        "StartDate": campaign.StartDate,
        "EndDate": campaign.EndDate,
        "Niche": campaign.Niche,
        "Goals": campaign.Goals,
        "Status": campaign.Status,
        "Flagged": campaign.Flagged,
        "SponsorID": campaign.SponsorID
    }
    
    advertisements = Advertisement.query.filter_by(CampaignID=campaign_id).all()
    
    file_path = f"{campaign_id}_campaign_details.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["Campaign Details"])
        writer.writerow(campaign_data.keys())
        writer.writerow(campaign_data.values())
        
        writer.writerow([])
        
        writer.writerow(["Advertisements"])
        if advertisements:
            ad_headers = ["AdvertisementID", "Amount", "FinalAmount", "Description", "Medium"]
            writer.writerow(ad_headers)
            for ad in advertisements:
                writer.writerow([ad.AdvertisementID, ad.Amount, ad.FinalAmount, ad.Description, ad.Medium])
        else:
            writer.writerow(["No advertisements found for this campaign"])
    
    return file_path  

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = celery_app.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is waiting for execution'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)



@celery_app.task()
def test_task():
    return "Celery is working!"

@celery_app.task()
def send_daily_reminders():
    influencers = Influencer.query.all()
    for influencer in influencers:
        if not has_visited_recently(influencer) or has_pending_ad_requests(influencer):
            send_alert(influencer)

@celery_app.task()
def send_monthly_activity_report():
    print("Starting to send monthly activity reports...")
    sponsors = Sponsor.query.filter_by(Flagged=False).all()
    print(f"Found {len(sponsors)} approved sponsors.")
    
    for sponsor in sponsors:
        print(f"Generating report for {sponsor.Email}...")
        report_data = generate_monthly_report(sponsor)
        
        if report_data is None:
            print(f"No report data generated for {sponsor.Email}. Skipping...")
            continue
        
        print(f"Sending report to {sponsor.Email}...")
        send_report_email(sponsor, report_data)
        print(f"Report sent to {sponsor.Email}: {report_data}")
    
    return {"msg": "Monthly activity report sent"}

@celery_app.task()
def export_campaign_details_as_csv(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return {"msg": "Campaign not found"}
    
    campaign_data = {
        "CampaignID": campaign.CampaignID,
        "Title": campaign.Title,
        "Description": campaign.Description,
        "Budget": campaign.Budget,
        "StartDate": campaign.StartDate,
        "EndDate": campaign.EndDate,
        "Niche": campaign.Niche,
        "Goals": campaign.Goals,
        "Status": campaign.Status,
        "Flagged": campaign.Flagged,
        "SponsorID": campaign.SponsorID
    }
    
    advertisements = Advertisement.query.filter_by(CampaignID=campaign_id).all()
    
    file_path = f"{campaign_id}_campaign_details.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["Campaign Details"])
        writer.writerow(campaign_data.keys())
        writer.writerow(campaign_data.values())
        
        writer.writerow([])
        
        writer.writerow(["Advertisements"])
        if advertisements:
            ad_headers = ["AdvertisementID", "Amount", "FinalAmount", "Description", "Medium"]
            writer.writerow(ad_headers)
            for ad in advertisements:
                writer.writerow([ad.AdvertisementID, ad.Amount, ad.FinalAmount, ad.Description, ad.Medium])
        else:
            writer.writerow(["No advertisements found for this campaign"])
    
    return {"msg": "Campaign details and advertisements exported as CSV", "file_path": file_path}

def has_visited_recently(influencer):
    now = datetime.utcnow()
    recent_campaign = Campaign.query.join(Request).filter(
        Request.SenderInfluencerID == influencer.InfluencerID,
        Request.DateRequested >= now - timedelta(days=1)
    ).first()
    return recent_campaign is not None

def has_pending_ad_requests(influencer):
    pending_requests = Request.query.filter(
        Request.ReceiverInfluencerID == influencer.InfluencerID,
        Request.Status == 'Pending'
    ).all()
    return len(pending_requests) > 0

def send_alert(influencer):
    pending_requests = Request.query.filter(
        Request.ReceiverInfluencerID == influencer.InfluencerID,
        Request.Status == 'Pending'
    ).join(Campaign).join(Advertisement).all()  

    message = render_template('reminder_mail.html', user=influencer, pending_requests=pending_requests)
    subject = "[REMINDER] Action Required"
    send_email(to_address=influencer.Email, subject=subject, message=message, content="html")

def generate_monthly_report(sponsor):
    campaigns = Campaign.query.filter_by(SponsorID=sponsor.SponsorID).all()
    report_data = {
        "sponsor": {
            "UserName": sponsor.UserName,
            "Email": sponsor.Email,
            "SponsorID": sponsor.SponsorID,
        },
        "campaigns": [],
        "total_budget": 0,
        "total_ads": 0,
        "total_spent": 0,
        "report_details": "This is your monthly report.",
    }

    for campaign in campaigns:
        report_data["total_budget"] += campaign.Budget
        
        advertisements = Advertisement.query.filter_by(CampaignID=campaign.CampaignID).all()
        report_data["total_ads"] += len(advertisements)
        
        for ad in advertisements:
            report_data["total_spent"] += ad.FinalAmount
        
        report_data["campaigns"].append({
            "CampaignID": campaign.CampaignID,
            "Title": campaign.Title,
            "Budget": campaign.Budget,
            "StartDate": campaign.StartDate.strftime('%Y-%m-%d'),
            "EndDate": campaign.EndDate.strftime('%Y-%m-%d'),
            "Status": campaign.Status,
            "Advertisements": [
                {
                    "AdvertisementID": ad.AdvertisementID,
                    "Amount": ad.Amount,
                    "FinalAmount": ad.FinalAmount,
                    "Description": ad.Description,
                    "Medium": ad.Medium,
                } for ad in advertisements
            ]
        })

    return report_data

def calculate_growth(sponsor):
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    current_campaigns = Campaign.query.filter(
        Campaign.SponsorID == sponsor.SponsorID,
        Campaign.StartDate >= datetime(current_year, current_month, 1),
        Campaign.EndDate <= datetime(current_year, current_month + 1, 1)
    ).all()

    current_sales = sum(campaign.Budget for campaign in current_campaigns)

    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1

    previous_campaigns = Campaign.query.filter(
        Campaign.SponsorID == sponsor.SponsorID,
        Campaign.StartDate >= datetime(previous_year, previous_month, 1),
        Campaign.EndDate <= datetime(previous_year, previous_month + 1, 1)
    ).all()

    previous_sales = sum(campaign.Budget for campaign in previous_campaigns)

    if previous_sales > 0:
        growth = ((current_sales - previous_sales) / previous_sales) * 100
    else:
        growth = 100 if current_sales > 0 else 0

    return growth

def send_report_email(sponsor, report_data):
    print(f"Sending monthly report to {sponsor.Email}")
    message = render_template('monthly_report_mail.html', report=report_data)
    subject = "[MONTHLY REPORT] Your Activity Report"
    send_email(to_address=sponsor.Email, subject=subject, message=message, content="html")

def send_email(to_address, subject, message, content="text", attachment_file=None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["To"] = to_address
    mail["Subject"] = subject
    
    if content == "html":
        mail.attach(MIMEText(message, "html"))
    else:
        mail.attach(MIMEText(message, "plain"))
    
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={attachment_file}")
        mail.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()
    return True

class Template:
    def __init__(self, template_string):
        self.template_string = template_string

    def render(self, **context):
        return self.template_string.format(**context)

# Schedule Celery tasks
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=11, hour=22),  
        send_daily_reminders.s(),
        name="send_daily_reminders"
    )
    sender.add_periodic_task(
        crontab(minute=11, hour=22, day_of_month=19),
        send_monthly_activity_report.s(),
        name="send_monthly_activity_report"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
