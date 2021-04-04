from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import ForeignKey


app = Flask(__name__)

app.config['SQLALACHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

colors = ('Red', 'Blue', 'Green', 'Yellow')


class Sailor(db.Model):
    sid = db.Column(db.Integer, nullable=False),
    sname = db.Column(db.String(40)),
    rating = db.Column(db.Integer, CheckConstraint(
        '1 < rating < 10', name='c_rating')),
    age = db.Column(db.Integer, CheckConstraint('age > 17', name='c_age')),
    PrimaryKeyConstraint('sid', name='c_sid')

    def __repr__(self):
        return f'{self.sid} - {self.sname}'


class Boat(db.Model):
    bid = db.Column(db.Integer, nullable=False),
    bname = db.Column(db.String(40)),
    color = db.Column(db.String(40), CheckConstraint(
        'color in colors', name='c_color')),
    PrimaryKeyConstraint('bid', name='c_bid')

    def __repr__(self):
        return f'{self.bid} - {self.bname}'


class Marina(db.Model):
    mid = db.Column(db.Integer, nullable=False),
    mname = db.Column(db.String(40), nullable=False),
    capacity = db.Column(db.Integer)
    PrimaryKeyConstraint('mid', name='c_mid')

    def __repr__(self):
        return f'{self.mid} - {self.mname}'


class Reservation(db.Model):
    sid = db.Column(db.Integer, ForeignKey(
        'Sailor.sid', ondelete="CASCADE"), nullable=False, ),
    bid = db.Column(db.Integer, ForeignKey(
        'Boat.bid', ondelete="CASCADE"), nullable=False),
    mid = db.Column(db.Integer, ForeignKey('Marina.mid', ondelete="SET NULL")),
    r_date = db.Column(db.String(12), nullable=False)
    PrimaryKeyConstraint('sid', 'bid', 'r_date', name='p_key')


@app.route('/')
def index():
    return 'Hello!'


@app.route('/sailors')
def get_sailors():
    sailors = Sailor.query.all()

    output = []
    for sailor in sailors:
        sailor_data = {'sid': sailor.sid, 'sname': sailor.sname,
                       'rating': sailor.rating, 'age': sailor.age}
        output.append(sailor_data)

    return {'sailors': output}


@app.route('/boats')
def get_boats():
    boats = Boat.query.all()

    output = []
    for boat in boats:
        boat_data = {'bid': boat.bid, 'bname': boat.bname, 'color': boat.color}
        output.append(boat_data)

    return {'boats': output}


@app.route('/marinas')
def get_marinas():
    marinas = Marina.query.all()

    output = []
    for marina in marinas:
        marina_data = {'mid': marina.mid,
                       'mname': marina.mname, 'capacity': marina.capacity}
        output.append(marina_data)

    return {'marinas': output}


@app.route('/reservations')
def get_reservations():
    reservations = Reservation.query.all()

    output = []
    for reservation in reservations:
        reservation_data = {'mid': reservation.mid,
                            'bid': reservation.bid, 'mid': reservation.mid, 'r_date': reservation.r_date}
        output.append(reservation_data)

    return {'reservations': output}
