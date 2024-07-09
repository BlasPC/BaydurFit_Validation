from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    country_of_origin = db.Column(db.String(100), default='Argentine')
    question_a = db.Column(db.Integer, default=1)
    question_b = db.Column(db.Integer, default=1)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time1 = db.Column(db.Float, nullable=False)
    time2 = db.Column(db.Float, nullable=False)
    paw1 = db.Column(db.Float, nullable=False)
    paw2 = db.Column(db.Float, nullable=False)
    pes1 = db.Column(db.Float, nullable=False)
    pes2 = db.Column(db.Float, nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class AccessTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    access_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
