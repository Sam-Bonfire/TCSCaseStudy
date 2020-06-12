from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'customer'
    ws_ssn = db.Column(db.Integer, unique=True)
    ws_cust_id = db.Column(db.Integer, primary_key=True)
    ws_name = db.Column(db.String(20))
    ws_adrs = db.Column(db.String(50))
    ws_age = db.Column(db.Integer)
