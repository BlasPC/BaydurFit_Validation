from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time1 = db.Column(db.Float, nullable=False)
    time2 = db.Column(db.Float, nullable=False)
    paw1 = db.Column(db.Float, nullable=False)
    paw2 = db.Column(db.Float, nullable=False)
    pes1 = db.Column(db.Float, nullable=False)
    pes2 = db.Column(db.Float, nullable=False)
