from flask import *
from flask_sqlalchemy import *

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

class Member(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

class Membership(db.Model):
    membership_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    price = db.Column(db.Integer)

class Tier(db.Model):
    tier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)