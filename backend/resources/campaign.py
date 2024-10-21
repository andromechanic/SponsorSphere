# resources/campaign.py
from flask_restful import Resource, reqparse, abort
from models import Campaign, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

campaign_args = reqparse.RequestParser()
campaign_args.add_argument("Title", type=str, help="Title of the campaign", required=True)
campaign_args.add_argument("Description", type=str, help="Description of the campaign", required=True)
campaign_args.add_argument("Budget", type=int, help="Budget for the campaign", required=True)
campaign_args.add_argument("StartDate", type=str, help="Start date of the campaign (ISO format)", required=True)
campaign_args.add_argument("EndDate", type=str, help="End date of the campaign (ISO format)", required=True)
campaign_args.add_argument("Niche", type=str, help="Niche of the campaign", required=True)
campaign_args.add_argument("Goals", type=str, help="Goals of the campaign", required=True)
campaign_args.add_argument("Status", type=str, help="Status of the campaign", default='Active')  # Optional

class CampaignAPI(Resource):
    @jwt_required()
    def post(self):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can create campaigns")

        args = campaign_args.parse_args()

        try:
            start_date = datetime.fromisoformat(args['StartDate'])
            end_date = datetime.fromisoformat(args['EndDate'])
        except ValueError:
            abort(400, message="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")

        campaign = Campaign(
            Title=args['Title'],
            Description=args['Description'],
            Budget=args['Budget'],
            StartDate=start_date,
            EndDate=end_date,
            Niche=args['Niche'],
            Goals=args['Goals'],
            Status=args.get('Status', 'Active'),
            SponsorID=sponsor_id
        )

        db.session.add(campaign)
        db.session.commit()

        return {'message': 'Campaign created successfully', 'CampaignID': campaign.CampaignID}, 201

    @jwt_required()
    def put(self, CampaignID):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can update campaigns")

        args = campaign_args.parse_args()
        campaign = Campaign.query.filter_by(CampaignID=CampaignID, SponsorID=sponsor_id).first()
        if not campaign:
            abort(404, message="Campaign not found or you do not have permission to update this campaign")

        try:
            if args.get('StartDate'):
                campaign.StartDate = datetime.fromisoformat(args['StartDate'])
            if args.get('EndDate'):
                campaign.EndDate = datetime.fromisoformat(args['EndDate'])
        except ValueError:
            abort(400, message="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")

        campaign.Title = args['Title'] if args['Title'] else campaign.Title
        campaign.Description = args['Description'] if args['Description'] else campaign.Description
        campaign.Budget = args['Budget'] if args['Budget'] else campaign.Budget
        campaign.Niche = args['Niche'] if args['Niche'] else campaign.Niche
        campaign.Goals = args['Goals'] if args['Goals'] else campaign.Goals
        campaign.Status = args['Status'] if args['Status'] else campaign.Status

        db.session.commit()

        return {'message': 'Campaign updated successfully'}, 200

    @jwt_required()
    def get(self, CampaignID=None):
        user_id, role = get_jwt_identity()

        if CampaignID is None:
            if role == "Sponsor":
                campaigns = Campaign.query.filter_by(SponsorID=user_id, Flagged=False).all()
            elif role == "Influencer":
                campaigns = Campaign.query.filter_by(Status='Active', Flagged=False).all()
            else:
                abort(403, message="Access forbidden: Invalid user role")

            return [{
                'CampaignID': campaign.CampaignID,
                'Title': campaign.Title,
                'Description': campaign.Description,
                'Budget': campaign.Budget,
                'StartDate': campaign.StartDate.isoformat(),
                'EndDate': campaign.EndDate.isoformat(),
                'Niche': campaign.Niche,
                'Goals': campaign.Goals,
                'Status': campaign.Status
            } for campaign in campaigns], 200

        if role == "Sponsor":
            campaign = Campaign.query.filter_by(CampaignID=CampaignID, SponsorID=user_id, Flagged=False).first()
        elif role == "Influencer":
            campaign = Campaign.query.filter_by(CampaignID=CampaignID, Status='Active', Flagged=False).first()
        else:
            abort(403, message="Access forbidden: Invalid user role")

        if not campaign:
            abort(404, message="Campaign not found or you do not have permission to view this campaign")

        return {
            'CampaignID': campaign.CampaignID,
            'Title': campaign.Title,
            'Description': campaign.Description,
            'Budget': campaign.Budget,
            'StartDate': campaign.StartDate.isoformat(),
            'EndDate': campaign.EndDate.isoformat(),
            'Niche': campaign.Niche,
            'Goals': campaign.Goals,
            'Status': campaign.Status
        }, 200

    @jwt_required()
    def delete(self, CampaignID):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can delete campaigns")

        campaign = Campaign.query.filter_by(CampaignID=CampaignID, SponsorID=sponsor_id, Flagged=False).first()
        if not campaign:
            abort(404, message="Campaign not found or you do not have permission to delete this campaign")

        db.session.delete(campaign)
        db.session.commit()

        return {'message': 'Campaign deleted successfully'}, 200

class SponsorFlaggedCampaignsAPI(Resource):
    @jwt_required()
    def get(self):
        user_id, role = get_jwt_identity()
        
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can view their flagged campaigns")

        flagged_campaigns = Campaign.query.filter_by(SponsorID=user_id, Flagged=True).all()

        return [{
            'CampaignID': campaign.CampaignID,
            'Title': campaign.Title,
            'Description': campaign.Description,
            'Budget': campaign.Budget,
            'StartDate': campaign.StartDate.isoformat(),
            'EndDate': campaign.EndDate.isoformat(),
            'Niche': campaign.Niche,
            'Goals': campaign.Goals,
            'Status': campaign.Status,
            'Flagged': True
        } for campaign in flagged_campaigns], 200

