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

def addMember(fname, lname, tier, price):
    with app.app_context():
        tier_num = 0
        if tier.lower() == "silver":
            tier_num = 1
        elif tier.lower() == "gold":
            tier_num = 2
        elif tier.lower() == "diamond":
            tier_num = 3
        else:
            print("Invalid tier name entered")
            exit()
        insert_member = Member(first_name=fname, last_name=lname)
        db.session.add(insert_member)
        db.session.commit()
        insert_membership = Membership(member_id=insert_member.member_id, price=price, tier_id=tier_num)
        db.session.add(insert_membership)
        db.session.commit()
    

def fetchMemberInfo():
    with app.app_context():
        db.session.commit()
        query = db.session.query(Member, Membership.price, Tier.name)\
                    .join(Membership, Member.member_id == Membership.member_id)\
                    .join(Tier, Membership.tier_id == Tier.tier_id).all()
        
        for member, price, tier_name in query:
            print(f"First Name: {member.first_name}, Last Name: {member.last_name}, Membership Price: {price}, Tier Name: {tier_name}")
if __name__ == '__main__':
    #addMember("Tony", "Soprano", "diamond", 150)
    fetchMemberInfo()