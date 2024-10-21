from flask_restful import Resource, reqparse, abort
from models import Request, Advertisement   
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from datetime import datetime, timedelta

request_args = reqparse.RequestParser()
request_args.add_argument("amount", type=int, help="Amount required", required=True)
request_args.add_argument("ad_id", type=int, help="Ad ID required", required=True)
request_args.add_argument("campaign_id", type=int, help="Campaign ID required", required=True)
request_args.add_argument("message", type=str, help="Optional message")


class RequestAPI(Resource):
    @jwt_required()
    def post(self):
        userdetails = get_jwt_identity()
        args = request_args.parse_args()

        user_id, user_role = userdetails

        request = Request(
            CampaignID=args['campaign_id'],
            AdvertisementID=args['ad_id'],
            ProposedAmount=args['amount'],
            Status='Pending',
            Message=args.get('message', ''),
            DateRequested=datetime.utcnow() 
        )

        if user_role == "Influencer":
            request.SenderInfluencerID = user_id
            request.ReceiverSponsorID = Advertisement.query.get(args['ad_id']).campaign.SponsorID
        elif user_role == "Sponsor":
            request.SenderSponsorID = user_id
        else:
            abort(403, message="Only sponsors or influencers can send ad requests.")

        db.session.add(request)
        db.session.commit()
        return {'message': f'Ad request created by {user_role.lower()} successfully', 'RequestID': request.RequestID}, 201

    @jwt_required()
    def get(self):
        try:
            userdetails = get_jwt_identity()
            user_id, user_role = userdetails

            if user_role == "Influencer":
                requests = Request.query.filter(
                    (Request.SenderInfluencerID == user_id) | (Request.ReceiverInfluencerID == user_id)
                ).all()
            elif user_role == "Sponsor":
                requests = Request.query.filter(
                    (Request.SenderSponsorID == user_id) | (Request.ReceiverSponsorID == user_id)
                ).all()
            else:
                abort(403, message="Only sponsors or influencers can view ad requests.")

            ist_offset = timedelta(hours=5, minutes=30)
            return [{
                'RequestID': req.RequestID,
                'Campaign': req.campaign.Title if req.campaign else None,
                'Advertisement': req.advertisement.Description if req.advertisement else None,
                'Influencer': req.sender_influencer.UserName if req.sender_influencer else None,
                'Proposed Amount': req.ProposedAmount,
                'Negotiated Amount': req.NegotiatedAmount,
                'Date Requested': (req.DateRequested + ist_offset).isoformat(),  # Convert to IST
                'Status': req.Status,
                'SenderSponsorID': req.SenderSponsorID,
                'SenderInfluencerID': req.SenderInfluencerID,
                'ReceiverInfluencerID': req.ReceiverInfluencerID,
                'ReceiverSponsorID': req.ReceiverSponsorID,
                'Message': req.Message,
                'DealDone': req.DealDone,
                'NegotiatedBy': req.NegotiatedBy
            } for req in requests], 200

        except Exception as e:
            print(f"Error occurred: {e}")
            abort(500, message="An internal server error occurred.")


class RequestActionAPI(Resource):
    @jwt_required()
    def post(self, request_id, action):
        userdetails = get_jwt_identity()
        user_id, user_role = userdetails

        request = Request.query.get(request_id)
        if not request:
            abort(404, message="Request not found.")

        if action == "accept":
            request.Status = 'Accepted'
        elif action == "decline":
            request.Status = 'Declined'
        elif action == "negotiate":
            negotiation_args = reqparse.RequestParser()
            negotiation_args.add_argument("amount", type=int, help="Negotiated amount required", required=True)
            negotiation_args.add_argument("message", type=str, help="Optional negotiation message")
            args = negotiation_args.parse_args()

            request.NegotiatedAmount = args['amount']
            request.Status = 'Pending' 
            request.Message = args.get('message', request.Message)  
            request.NegotiatedBy = 'Sponsor' if user_role == 'Sponsor' else 'Influencer' 
        else:
            abort(400, message="Invalid action. Use 'accept', 'decline', or 'negotiate'.")

        db.session.commit()
        return {
            'message': f'Request {action}ed successfully', 
            'RequestID': request_id,
            'NegotiatedAmount': request.NegotiatedAmount,
            'NegotiatedBy': request.NegotiatedBy
        }, 200


class SponsorRequestToInfluencerAPI(Resource):
    @jwt_required()
    def post(self, influencer_id):
        userdetails = get_jwt_identity()
        user_id, user_role = userdetails

        if user_role != "Sponsor":
            abort(403, message="Only sponsors can send requests to influencers.")

        args = request_args.parse_args()

        request = Request(
            SenderSponsorID=user_id,
            ReceiverInfluencerID=influencer_id,
            CampaignID=args['campaign_id'],
            AdvertisementID=args['ad_id'],
            ProposedAmount=args['amount'],
            Status='Pending',
            Message=args.get('message', ''),
            DateRequested=datetime.utcnow()
        )

        db.session.add(request)
        db.session.commit()
        return {'message': 'Ad request sent to influencer successfully', 'RequestID': request.RequestID}, 201

from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Request, db

class InfluencerNegotiationAPI(Resource):
    @jwt_required()
    def put(self, request_id):
        userdetails = get_jwt_identity()
        user_id, user_role = userdetails

        if user_role != "Influencer":
            abort(403, message="Only influencers can negotiate.")

        request = Request.query.get(request_id)
        if not request:
            abort(404, message="Request not found.")

        negotiation_args = reqparse.RequestParser()
        negotiation_args.add_argument("amount", type=int, help="Negotiated amount required", required=True)
        negotiation_args.add_argument("message", type=str, help="Optional negotiation message")
        args = negotiation_args.parse_args()

        new_amount = args['amount']

        if request.NegotiatedAmount is not None and new_amount == request.NegotiatedAmount:
            request.DealDone = True
            status_message = "Deal finalized"
        else:
            request.DealDone = False
            status_message = "Negotiation updated"

        request.NegotiatedAmount = new_amount
        request.Status = 'Pending' 
        request.Message = args.get('message', request.Message)  
        request.NegotiatedBy = 'Influencer'  

        db.session.commit()

        return {
            'message': f'{status_message} successfully', 
            'RequestID': request_id,
            'NegotiatedAmount': new_amount,
            'DealDone': request.DealDone,
            'NegotiatedBy': request.NegotiatedBy
        }, 200
