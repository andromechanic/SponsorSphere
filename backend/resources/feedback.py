# backend/resources/feedback.py
from flask_restful import Resource, reqparse, abort
from models import Feedback, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from extensions import cache

feedback_args = reqparse.RequestParser()
feedback_args.add_argument("Rating", type=int, help="Rating required", required=True)
feedback_args.add_argument("Comment", type=str, help="Comment required", required=True)
feedback_args.add_argument("InfluencerID", type=int, help="Influencer ID required", required=True)

class FeedbackResource(Resource):
    @jwt_required()
    def post(self):
        args = feedback_args.parse_args()
        current_user_id, user_role = get_jwt_identity()

        if user_role != "Sponsor":
            abort(403, message="Only sponsors can submit feedback for influencers")

        feedback = Feedback(
            Rating=args['Rating'],
            Comment=args['Comment'],
            SponsorID=current_user_id,
            InfluencerID=args['InfluencerID'],
        )

        db.session.add(feedback)
        db.session.commit()

        return {'message': 'Feedback submitted successfully', 'FeedbackID': feedback.FeedbackID}, 201

    @jwt_required()
    @cache.cached(timeout = 300)
    def get(self, influencer_id):
        feedback_list = Feedback.query.filter_by(InfluencerID=influencer_id).all()
        if not feedback_list:
            abort(404, message="No feedback found for this influencer")

        feedback_data = [{
            'FeedbackID': feedback.FeedbackID,
            'Rating': feedback.Rating,
            'Comment': feedback.Comment,
            'DateSubmitted': feedback.DateSubmitted.isoformat(),
            'SponsorID': feedback.SponsorID,
        } for feedback in feedback_list]

        return {'feedback': feedback_data}, 200

    @jwt_required()
    def get_average_rating(self, influencer_id):
        average_rating = db.session.query(func.avg(Feedback.Rating)).filter(Feedback.InfluencerID == influencer_id).scalar()

        if average_rating is None:
            return {'message': 'No ratings found for this influencer'}, 404

        rating_count = Feedback.query.filter_by(InfluencerID=influencer_id).count()

        return {
            'influencer_id': influencer_id,
            'average_rating': float(round(average_rating, 2)),
            'rating_count': rating_count
        }, 200

class AverageRatingResource(Resource):
    @jwt_required()
    def get(self, influencer_id):
        return FeedbackResource().get_average_rating(influencer_id)
