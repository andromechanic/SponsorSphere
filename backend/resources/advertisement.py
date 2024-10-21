from flask_restful import Resource, reqparse, abort
from models import Advertisement, Campaign, db, Sponsor
from flask_jwt_extended import jwt_required, get_jwt_identity

advertisement_args = reqparse.RequestParser()
advertisement_args.add_argument("Amount", type=int, help="Amount required", required=True)
advertisement_args.add_argument("FinalAmount", type=int, help="Final amount required", required=True)
advertisement_args.add_argument("Description", type=str, help="Description required", required=True)
advertisement_args.add_argument("Medium", type=str, help="Medium required", required=True)
advertisement_args.add_argument("CampaignID", type=int, help="Campaign ID required", required=True)

class AdvertisementAPI(Resource):
    @jwt_required()
    def post(self):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can create advertisements")

        args = advertisement_args.parse_args()

        campaign = Campaign.query.filter_by(CampaignID=args['CampaignID'], SponsorID=sponsor_id, Flagged=False).first()
        if not campaign:
            abort(404, message="Campaign not found, flagged, or you do not have permission to create an advertisement for this campaign")

        advertisement = Advertisement(
            Amount=args['Amount'],
            FinalAmount=args['FinalAmount'],
            Description=args['Description'],
            Medium=args['Medium'],
            CampaignID=args['CampaignID']
        )

        db.session.add(advertisement)
        db.session.commit()

        return {'message': 'Advertisement created successfully', 'AdvertisementID': advertisement.AdvertisementID}, 201

    @jwt_required()
    def put(self, AdvertisementID):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can update advertisements")

        args = advertisement_args.parse_args()
        advertisement = Advertisement.query.join(Campaign).filter(
            Advertisement.AdvertisementID == AdvertisementID,
            Campaign.SponsorID == sponsor_id,
            Campaign.Flagged == False
        ).first()

        if not advertisement:
            abort(404, message="Advertisement not found, campaign flagged, or you do not have permission to update this advertisement")

        advertisement.Amount = args['Amount']
        advertisement.FinalAmount = args['FinalAmount']
        advertisement.Description = args['Description']
        advertisement.Medium = args['Medium']
        advertisement.CampaignID = args['CampaignID']

        db.session.commit()

        return {'message': 'Advertisement updated successfully'}, 200

    @jwt_required()
    def get(self, AdvertisementID):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can view advertisements")

        advertisement = Advertisement.query.join(Campaign).filter(
            Advertisement.AdvertisementID == AdvertisementID,
            Campaign.SponsorID == sponsor_id,
            Campaign.Flagged == False
        ).first()

        if not advertisement:
            abort(404, message="Advertisement not found, campaign flagged, or you do not have permission to view this advertisement")

        return {
            'AdvertisementID': advertisement.AdvertisementID,
            'Amount': advertisement.Amount,
            'FinalAmount': advertisement.FinalAmount,
            'Description': advertisement.Description,
            'Medium': advertisement.Medium,
            'CampaignID': advertisement.CampaignID
        }, 200

    @jwt_required()
    def delete(self, AdvertisementID):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can delete advertisements")

        advertisement = Advertisement.query.join(Campaign).filter(
            Advertisement.AdvertisementID == AdvertisementID,
            Campaign.SponsorID == sponsor_id,
            Campaign.Flagged == False
        ).first()

        if not advertisement:
            abort(404, message="Advertisement not found, campaign flagged, or you do not have permission to delete this advertisement")

        db.session.delete(advertisement)
        db.session.commit()

        return {'message': 'Advertisement deleted successfully'}, 200

    @jwt_required()
    def get(self, CampaignID):
        sponsor_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can view advertisements")

        advertisements = Advertisement.query.join(Campaign).filter(
            Advertisement.CampaignID == CampaignID,
            Campaign.SponsorID == sponsor_id,
            Campaign.Flagged == False
        ).all()

        if not advertisements:
            abort(404, message="No advertisements found for this campaign or the campaign is flagged")

        return [{
            'AdvertisementID': ad.AdvertisementID,
            'Amount': ad.Amount,
            'FinalAmount': ad.FinalAmount,
            'Description': ad.Description,
            'Medium': ad.Medium,
            'CampaignID': ad.CampaignID
        } for ad in advertisements], 200

class InfluencerAdsAPI(Resource):
    @jwt_required()
    def get(self):
        influencer_id, role = get_jwt_identity()
        if role != "Influencer":
            abort(403, message="Access forbidden: Only Influencers can view advertisements")

        advertisements = Advertisement.query.join(Campaign).join(Sponsor).filter(
            Campaign.Flagged == False,
            Campaign.Status == 'Active'
        ).all()

        if not advertisements:
            abort(404, message="No advertisements found")

        result = []
        for ad in advertisements:
            result.append({
                'AdvertisementID': ad.AdvertisementID,
                'Amount': ad.Amount,
                'FinalAmount': ad.FinalAmount,
                'Description': ad.Description,
                'Medium': ad.Medium,
                'CampaignID': ad.CampaignID,
                'CampaignTitle': ad.campaign.Title,
                'SponsorName': ad.campaign.sponsor.CompanyName,
            })

        return result, 200
