from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#notes for name and vr type
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#a user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

#hours and schedule will have one to one 
class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hourss = db.Column(db.String(150))
#a schedule model
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    startTime = db.Column(db.String(150))
    hours = db.Column(db.String(150))