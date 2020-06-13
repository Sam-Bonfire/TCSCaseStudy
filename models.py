from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'userstore'
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(35))
    password = db.Column(db.String(100))
    type = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime)

    def __init__(self, user_login, password, type):
        self.user_login = user_login
        self.password = password
        self.type = type


class Customer(db.Model):
    ws_ssn = db.Column(db.Integer, unique=True)
    ws_cust_id = db.Column(db.Integer, primary_key=True)
    ws_name = db.Column(db.String(20))
    ws_adrs = db.Column(db.String(50))
    ws_age = db.Column(db.Integer)


class Account(db.Model):
    act_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ws_cust_id = db.Column(db.Integer)
    ws_acct_type = db.Column(db.String(1))
    ws_acct_balance = db.Column(db.Integer)
    ws_acct_crdate = db.Column(db.Date)
    ws_acct_lasttrdate = db.Column(db.Date)
    ws_acct_duration = db.Column(db.Integer)


class Transaction(db.Model):
    trxn_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ws_cust_id = db.Column(db.Integer)
    ws_acct_type = db.Column(db.String(1))
    ws_amt = db.Column(db.Integer)
    ws_trxn_date = db.Column(db.Date)
    ws_src_typ = db.Column(db.String(1))
    ws_tgt_typ = db.Column(db.String(1))
