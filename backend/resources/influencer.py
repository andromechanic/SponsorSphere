# resources/influencer.py
from flask_restful import Resource, reqparse, abort
from models import Influencer
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from flask import request
from werkzeug.utils import secure_filename

influencer_signup_args = reqparse.RequestParser()
influencer_signup_args.add_argument("UserName", type=str, help="UserName required", required=True)
influencer_signup_args.add_argument("Email", type=str, help="Email required", required=True)
influencer_signup_args.add_argument("Password", type=str, help="Password required", required=True)
influencer_signup_args.add_argument("Platforms", type=str, help="Platforms required")
influencer_signup_args.add_argument("Niche", type=str, help="Niche required", required=True)

influencer_login_args = reqparse.RequestParser()
influencer_login_args.add_argument("UserName", type=str, help="UserName required", required=True)
influencer_login_args.add_argument("Password", type=str, help="Password required", required=True)

class InfluencerSignUp(Resource):
    def post(self):
        args = influencer_signup_args.parse_args()
        UserName = args['UserName']
        Email = args['Email']
        
        user = Influencer.query.filter((Influencer.UserName == UserName) | (Influencer.Email == Email)).first()
        if user:
            abort(409, message="Username or Email already exists")
        
        hashed_password = generate_password_hash(args['Password'], method='pbkdf2:sha256')
        
        user = Influencer(
            UserName=UserName,
            Email=Email,
            Password=hashed_password,
            Platforms=args['Platforms'],
            Niche=args['Niche'],
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {'UserName': UserName, 'message': 'Influencer created successfully'}, 201

class InfluencerLogin(Resource):
    def post(self):
        args = influencer_login_args.parse_args()
        UserName = args['UserName']
        Password = args['Password']
        
        user = Influencer.query.filter_by(UserName=UserName).first()
        
        if user and check_password_hash(user.Password, Password):
            if user.Flagged:
                return {'message': 'Your account has been flagged. Please contact admin at admin@sponsorsphere.com.'}, 403
            token = create_access_token(identity=[user.InfluencerID, "Influencer"])
            return {'token': token, 'UserName': UserName, 'User': "Influencer"}, 200
        else:
            return {'message': 'Invalid Username or Password'}, 401

class InfluencerProfile(Resource):
    def get(self):
        influencers = Influencer.query.all() 
        influencer_list = []
        
        for influencer in influencers:
            influencer_list.append({
                'UserName': influencer.UserName,
                'Email': influencer.Email,
                'Platforms': influencer.Platforms,
                'Niche': influencer.Niche,
                'Followers': influencer.Followers,
                'ProfilePic': influencer.ProfilePic,
                'AverageRating': influencer.AverageRating,
                'InfluencerID': influencer.InfluencerID,
            })
        
        return influencer_list, 200

class InfluencerUpdateProfile(Resource):
    @jwt_required()
    def get(self):
        current_user_id, role = get_jwt_identity()
        if role != "Influencer":
            abort(403, message="Access forbidden: Only Influencers can access this resource")
        influencer = Influencer.query.filter_by(InfluencerID=current_user_id).first()
        if not influencer:
            abort(404, message="Influencer not found")
        return {
            'UserName': influencer.UserName,
            'Email': influencer.Email,
            'Password': '',  
            'Platforms': influencer.Platforms,
            'Niche': influencer.Niche,
            'Followers': influencer.Followers,
            'Reach': influencer.Reach,
            'ProfilePic': influencer.ProfilePic,
            'AverageRating': influencer.AverageRating,
            'TotalEarning': influencer.TotalEarning,
            'InfluencerID': influencer.InfluencerID,
        }, 200

    @jwt_required()
    def put(self):
        current_user_id, role = get_jwt_identity()
        if role != "Influencer":
            abort(403, message="Access forbidden: Only Influencers can access this resource")
        influencer = Influencer.query.filter_by(InfluencerID=current_user_id).first()
        if not influencer:
            abort(404, message="Influencer not found")
        influencer.UserName = request.form.get('UserName', influencer.UserName)
        influencer.Email = request.form.get('Email', influencer.Email)
        password = request.form.get('Password')
        if password:
            influencer.Password = generate_password_hash(password, method='pbkdf2:sha256')
        
        influencer.Platforms = request.form.get('Platforms', influencer.Platforms)
        influencer.Niche = request.form.get('Niche', influencer.Niche)
        influencer.Followers = request.form.get('Followers', influencer.Followers) or influencer.Followers
        influencer.Reach = request.form.get('Reach', influencer.Reach) or influencer.Reach
        
        if 'ProfilePic' in request.files:
            file = request.files['ProfilePic']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
            directory = 'static/profile_pics'
            
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, filename)
            file.save(file_path)
            influencer.ProfilePic = f'/static/profile_pics/{filename}'  

        db.session.commit()
        
        return {'message': 'Profile updated successfully'}, 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
