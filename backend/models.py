from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)

class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    SponsorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    UserName = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    CompanyName = db.Column(db.String(255), nullable=False)
    Industry = db.Column(db.String(255))
    CompanyLogo = db.Column(db.String(255))
    Approved = db.Column(db.Boolean, nullable=False, default=False)
    Flagged = db.Column(db.Boolean, nullable=False, default=True)

    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    sent_requests = db.relationship('Request', backref='sender_sponsor', lazy=True, foreign_keys='Request.SenderSponsorID')
    received_requests = db.relationship('Request', backref='receiver_sponsor', lazy=True, foreign_keys='Request.ReceiverSponsorID')
    feedbacks = db.relationship('Feedback', backref='sponsor', lazy=True)

class Influencer(db.Model):
    __tablename__ = 'influencer'
    InfluencerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    UserName = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Platforms = db.Column(db.String(255), nullable=False)
    Niche = db.Column(db.String(255), nullable=False)
    Followers = db.Column(db.Integer, nullable=False, default=0)
    Reach = db.Column(db.Integer, nullable=False, default=0)
    TotalEarning = db.Column(db.Integer, nullable=False, default=0)
    MonthlyEarning = db.Column(db.Integer, nullable=False, default=0)
    ProfilePic = db.Column(db.String(255))
    AverageRating = db.Column(db.Float, default=0)
    Flagged = db.Column(db.Boolean, nullable=False, default=False)

    sent_requests = db.relationship('Request', backref='sender_influencer', lazy=True, foreign_keys='Request.SenderInfluencerID')
    received_requests = db.relationship('Request', backref='receiver_influencer', lazy=True, foreign_keys='Request.ReceiverInfluencerID')
    feedbacks = db.relationship('Feedback', backref='influencer', lazy=True)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    CampaignID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Budget = db.Column(db.Integer, nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    Niche = db.Column(db.String(255), nullable=False)
    Goals = db.Column(db.Text, nullable=False)
    Status = db.Column(db.String(50), nullable=False, default='Active')
    Flagged = db.Column(db.Boolean, nullable=False, default=False)

    SponsorID = db.Column(db.Integer, db.ForeignKey('sponsor.SponsorID'), nullable=False)

    advertisements = db.relationship('Advertisement', backref='campaign', lazy=True)
    requests = db.relationship('Request', backref='campaign', lazy=True)

class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    AdvertisementID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Amount = db.Column(db.Integer, nullable=False)
    FinalAmount = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Medium = db.Column(db.String(50), nullable=False)

    CampaignID = db.Column(db.Integer, db.ForeignKey('campaign.CampaignID'), nullable=False)

    requests = db.relationship('Request', backref='advertisement', lazy=True)

class Request(db.Model):
    __tablename__ = 'request'
    RequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Status = db.Column(db.String(50), nullable=False, default='Pending')
    DateRequested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ProposedAmount = db.Column(db.Integer, nullable=False)
    NegotiatedAmount = db.Column(db.Integer, nullable=True)  
    Message = db.Column(db.Text)
    
    SenderInfluencerID = db.Column(db.Integer, db.ForeignKey('influencer.InfluencerID'), nullable=True)
    SenderSponsorID = db.Column(db.Integer, db.ForeignKey('sponsor.SponsorID'), nullable=True)
    ReceiverInfluencerID = db.Column(db.Integer, db.ForeignKey('influencer.InfluencerID'), nullable=True)
    ReceiverSponsorID = db.Column(db.Integer, db.ForeignKey('sponsor.SponsorID'), nullable=True)
    DealDone = db.Column(db.Boolean, nullable=False, default=False)
    AdvertisementID = db.Column(db.Integer, db.ForeignKey('advertisement.AdvertisementID'), nullable=False)
    CampaignID = db.Column(db.Integer, db.ForeignKey('campaign.CampaignID'), nullable=False)
    NegotiatedBy = db.Column(db.String(20), nullable=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    FeedbackID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.Text, nullable=False)
    DateSubmitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    InfluencerID = db.Column(db.Integer, db.ForeignKey('influencer.InfluencerID'), nullable=True)
    SponsorID = db.Column(db.Integer, db.ForeignKey('sponsor.SponsorID'), nullable=True)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
