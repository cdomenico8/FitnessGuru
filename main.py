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
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'))
    price = db.Column(db.Integer)
    tier_id = db.Column(db.Integer)
    member = db.relationship('Member', backref=db.backref('memberships', lazy=True))

class Tier(db.Model):
    tier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

def fetchMemberInfo():
    with app.app_context():
        # Joining Member, Membership, and Tier tables
        query = db.session.query(Member, Membership.price, Tier.name)\
                    .join(Membership, Member.member_id == Membership.member_id)\
                    .join(Tier, Membership.tier_id == Tier.tier_id).all()
        
        for member, price, tier_name in query:
            print(f"First Name: {member.first_name}, Last Name: {member.last_name}, Membership Price: {price}, Tier Name: {tier_name}")
if __name__ == '__main__':
    fetchMemberInfo()