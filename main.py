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

class Snacks(db.Model):
    snack_id = db.Column(db.Integer, primary_key=True)
    snack_name = db.Column(db.String)
    snack_count = db.Column(db.Integer)
    unit_price = db.Column(db.Float)

@app.route('/')
def member_management():
    members_info = fetchMemberInfo()
    return render_template('Members.html', members=members_info)

@app.route('/classes')
def classes():
    return render_template('ClassSchedule.html')

@app.route('/snacks')
def snacks():
    snacks_info = fetchSnackInfo()
    return render_template('Snacks.html', snacks=snacks_info)

# this will be used for member management to add members
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
    
#this shows a member's name, tier, and price
#will probably have to add query results to a array to display on webpage
def fetchMemberInfo():
    with app.app_context():
        #db.session.commit()
        query = db.session.query(Member, Membership.price, Tier.name)\
                    .join(Membership, Member.member_id == Membership.member_id)\
                    .join(Tier, Membership.tier_id == Tier.tier_id).all()
        
        members_info = []
        for member, price, tier_name in query:
            member_info = {
                'first_name': member.first_name,
                'last_name': member.last_name,
                'price': price,
                'tier_name': tier_name
            }
            members_info.append(member_info)
    return members_info

# this will be used for snack management to view inventory
#will probably have to add query results to a array to display on webpage
def fetchSnackInfo():
    with app.app_context():
        #db.session.commit()
        query = db.session.query(Snacks).all()
        snacks_info = []
        for snack in query:
            snack_info = {
                'snack_name': snack.snack_name,
                'snack_count': snack.snack_count,
                'unit_price': snack.unit_price
            }
            snacks_info.append(snack_info)
    return snacks_info
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)