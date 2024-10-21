# resources/sponsor.py
from flask_restful import Resource, reqparse, abort
from models import Sponsor
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

sponsor_signup_args = reqparse.RequestParser()
sponsor_signup_args.add_argument("UserName", type=str, help="UserName required", required=True)
sponsor_signup_args.add_argument("Email", type=str, help="Email required", required=True)
sponsor_signup_args.add_argument("Password", type=str, help="Password required", required=True)
sponsor_signup_args.add_argument("CompanyName", type=str, help="Company Name required", required=True)
sponsor_signup_args.add_argument("Industry", type=str, help="Industry required", required=True)

sponsor_login_args = reqparse.RequestParser()
sponsor_login_args.add_argument("UserName", type=str, help="UserName required", required=True)
sponsor_login_args.add_argument("Password", type=str, help="Password required", required=True)

class SponsorSignUp(Resource):
    def post(self):
        args = sponsor_signup_args.parse_args()
        UserName = args['UserName']
        Email = args['Email']
        
        user = Sponsor.query.filter((Sponsor.UserName == UserName) | (Sponsor.Email == Email)).first()
        if user:
            abort(409, message="Username or Email already exists")
        
        hashed_password = generate_password_hash(args['Password'], method='pbkdf2:sha256')
        
        user = Sponsor(
            UserName=UserName,
            Email=Email,
            Password=hashed_password,
            CompanyName=args['CompanyName'],
            Industry=args['Industry'],
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {'UserName': UserName, 'message': 'Signup Complete! Account is sent for approval to the admin '}, 201

class SponsorLogin(Resource):
    def post(self):
        args = sponsor_login_args.parse_args()
        UserName = args['UserName']
        Password = args['Password']
        
        user = Sponsor.query.filter_by(UserName=UserName).first()
        
        if user and check_password_hash(user.Password, Password):
            if user.Flagged:
                return {'message': 'Your account has not been approved. Please contact support.'}, 403
            token = create_access_token(identity=[user.SponsorID, "Sponsor"])
            return {
                'token': token,
                'UserName': user.UserName,
                'Email': user.Email,
                'CompanyName': user.CompanyName,
                'Industry': user.Industry,
                'Approved': user.Approved,
                'SponsorID': user.SponsorID,
                'User': "Sponsor"
            }, 200
        else:
            return {'message': 'Invalid Username or Password'}, 401

class SponsorProfile(Resource):
    @jwt_required()  
    def get(self):
        current_user_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can access this resource")

        sponsor = Sponsor.query.filter_by(SponsorID=current_user_id).first()
        if not sponsor:
            abort(404, message="Sponsor not found")
        return {
            'UserName': sponsor.UserName,
            'Email': sponsor.Email,
            'CompanyName': sponsor.CompanyName,
            'Industry': sponsor.Industry,
            'Approved': sponsor.Approved,
            'SponsorID': sponsor.SponsorID 
        }, 200

class SponsorUpdateProfile(Resource):
    @jwt_required()  
    def put(self):
        current_user_id, role = get_jwt_identity()
        if role != "Sponsor":
            abort(403, message="Access forbidden: Only Sponsors can access this resource")

        args = sponsor_signup_args.parse_args()
        sponsor = Sponsor.query.filter_by(SponsorID=current_user_id).first()
        
        if not sponsor:
            abort(404, message="Sponsor not found")
        
        sponsor.UserName = args['UserName'] if args['UserName'] else sponsor.UserName
        sponsor.Email = args['Email'] if args['Email'] else sponsor.Email
        sponsor.CompanyName = args['CompanyName'] if args['CompanyName'] else sponsor.CompanyName
        sponsor.Industry = args['Industry'] if args['Industry'] else sponsor.Industry
        
        db.session.commit()
        
        return {'message': 'Profile updated successfully'}, 200
