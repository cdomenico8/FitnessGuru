from flask import *
from flask_sqlalchemy import *
from sqlalchemy import func

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db?check_same_thread=False"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
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

@app.route('/update_member')
def update_member():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    tier_name = request.args.get('tier_name')
    price = request.args.get('price')
    return render_template('update_member.html',first_name=first_name, last_name=last_name, tier_name=tier_name, price=price)

@app.route('/updateMember', methods=['POST'])
def updateMember():
    fname = request.form.get('first_name')
    lname = request.form.get('last_name')
    tier = request.form.get('tier_name')
    price = request.form.get('price')
    updateMember(fname, lname, tier, price)
    return redirect('/')

@app.route('/classes')
def classes():
    return render_template('ClassSchedule.html')

@app.route('/snacks')
def snacks():
    snacks_info = fetchSnackInfo()
    return render_template('Snacks.html', snacks=snacks_info)

@app.route('/addsnack', methods=['POST'])
def addsnack():
    name = request.form.get('name')
    price = float(request.form.get('price'))
    count = int(request.form.get('count'))
    addSnack(name, price, count)
    return redirect('/snacks')


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

def updateMember(fname, lname, tier, price):
    with app.app_context():
        fname = fname.strip()
        lname = lname.strip()
        #find member in Member db
        member = Member.query.filter(func.lower(Member.first_name) == func.lower(fname), 
                             func.lower(Member.last_name) == func.lower(lname)).first()
        if member:
            #update member info -> this will need to be changed
            member.first_name=fname
            member.last_name=lname
            db.session.commit()
            #fetch new tier to get new tier_id
            get_tier = Tier.query.filter_by(name=tier).first()
            if get_tier:
                #find membership entry based on member_id
                membership = Membership.query.filter_by(member_id=member.member_id).first()
                if membership:
                    #update membership info
                    membership.tier_id = get_tier.tier_id
                    membership.price = price
                    db.session.commit()
                else:
                    print("Error: unable to fetch membership")
            else:
                print("Error: unable to fetch tier")
        else:
            print("Error: unable to fetch member")
    
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

def addSnack(name, price, count):
    with app.app_context():
        add_snack = Snacks(snack_name=name, snack_count=count, unit_price=price)
        db.session.add(add_snack)
        db.session.commit()
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)