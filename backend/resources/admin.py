from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models import Admin, Campaign, Sponsor, Influencer, db
from sqlalchemy import func
from datetime import datetime

admin_login_args = reqparse.RequestParser()
admin_login_args.add_argument("UserName", type=str, help="UserName required", required=True)
admin_login_args.add_argument("Password", type=str, help="Password required", required=True)

class AdminLogin(Resource):
    def post(self):
        args = admin_login_args.parse_args()
        UserName = args['UserName']
        Password = args['Password']
        
        user = Admin.query.filter_by(UserName=UserName).first()
        
        if user and check_password_hash(user.Password, Password):
            token = create_access_token(identity=[user.AdminID, "Admin"])
            return {'token': token, 'UserName': UserName, 'User': "Admin"}, 200
        else:
            return {'message': 'Invalid Username or Password'}, 401

class OngoingCampaigns(Resource):
    @jwt_required()
    def get(self):
        current_date = datetime.utcnow()
        campaigns = Campaign.query.all()
        
        return [{
            'CampaignID': c.CampaignID,
            'Title': c.Title,
            'SponsorName': c.sponsor.CompanyName,
            'StartDate': c.StartDate.isoformat(),
            'EndDate': c.EndDate.isoformat(),
            'Status': c.Status
        } for c in campaigns], 200

class FlaggedItems(Resource):
    @jwt_required()
    def get(self):
        flagged_sponsors = Sponsor.query.filter_by(Flagged=True).all()
        flagged_influencers = Influencer.query.filter_by(Flagged=True).all()
        flagged_campaigns = Campaign.query.filter_by(Flagged=True).all()
        
        flagged_items = []
        for s in flagged_sponsors:
            flagged_items.append({
                'ID': s.SponsorID,
                'Type': 'Sponsor',
                'Name': s.CompanyName,
                'Reason': 'Admin flagged'  
            })
        for i in flagged_influencers:
            flagged_items.append({
                'ID': i.InfluencerID,
                'Type': 'Influencer',
                'Name': i.UserName,
                'Reason': 'Admin flagged'
            })
        for c in flagged_campaigns:
            flagged_items.append({
                'ID': c.CampaignID,
                'Type': 'Campaign',
                'Name': c.Title,
                'Reason': 'Admin flagged'
            })
        
        return flagged_items, 200

class FlagItem(Resource):
    @jwt_required()
    def post(self, item_type, item_id):
        try:
            item_type = item_type.lower()  
            if item_type == 'sponsor':
                item = Sponsor.query.get(item_id)
            elif item_type == 'influencer':
                item = Influencer.query.get(item_id)
            elif item_type == 'campaign':
                item = Campaign.query.get(item_id)
            else:
                return {'message': f'Invalid item type: {item_type}'}, 400
            
            if not item:
                return {'message': f'{item_type.capitalize()} with ID {item_id} not found'}, 404
            
            item.Flagged = True
            db.session.commit()
            return {'message': f'{item_type.capitalize()} flagged successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error flagging {item_type}: {str(e)}'}, 500

class UnflagItem(Resource):
    @jwt_required()
    def post(self, item_type, item_id):
        if item_type == 'Sponsor':
            item = Sponsor.query.get(item_id)
        elif item_type == 'Influencer':
            item = Influencer.query.get(item_id)
        elif item_type == 'Campaign':
            item = Campaign.query.get(item_id)
        else:
            return {'message': 'Invalid item type'}, 400
        
        if not item:
            return {'message': 'Item not found'}, 404
        
        item.Flagged = False
        db.session.commit()
        return {'message': f'{item_type} unflagged successfully'}, 200

class Statistics(Resource):
    @jwt_required()
    def get(self):
        total_sponsors = Sponsor.query.count()
        total_influencers = Influencer.query.count()
        total_campaigns = Campaign.query.count()
        
        current_date = datetime.utcnow()
        ongoing_campaigns = Campaign.query.filter(
            Campaign.StartDate <= current_date,
            Campaign.EndDate >= current_date
        ).count()
        
        flagged_campaigns = Campaign.query.filter_by(Flagged=True).count()
        
        avg_budget = db.session.query(func.avg(Campaign.Budget)).scalar()
        
        top_niches = db.session.query(
            Influencer.Niche, func.count(Influencer.Niche)
        ).group_by(Influencer.Niche).order_by(func.count(Influencer.Niche).desc()).limit(5).all()
        
        return {
            'total_sponsors': total_sponsors,
            'total_influencers': total_influencers,
            'total_campaigns': total_campaigns,
            'ongoing_campaigns': ongoing_campaigns,
            'flagged_campaigns': flagged_campaigns,
            'average_budget': float(avg_budget) if avg_budget else 0,
            'top_niches': [{'niche': niche, 'count': count} for niche, count in top_niches]
        }, 200

class AllUsers(Resource):
    @jwt_required()
    def get(self):
        sponsors = Sponsor.query.all()
        influencers = Influencer.query.all()
        
        all_users = []
        for s in sponsors:
            all_users.append({
                'ID': s.SponsorID,
                'Type': 'Sponsor',
                'Name': s.CompanyName,
                'Flagged': s.Flagged
            })
        for i in influencers:
            all_users.append({
                'ID': i.InfluencerID,
                'Type': 'Influencer',
                'Name': i.UserName,
                'Flagged': i.Flagged
            })
        
        return all_users, 200
