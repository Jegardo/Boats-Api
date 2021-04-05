from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data.db'
db = SQLAlchemy(app)


class Sailor(db.Model):
    __tablename__ = 'sailor'

    sid = db.Column(db.Integer, primary_key=True, nullable=False)
    sname = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, db.CheckConstraint(
        '1 < rating < 10', name='c_rating'))
    age = db.Column(db.Integer, db.CheckConstraint('age > 17', name='c_age'))
    db.PrimaryKeyConstraint('sid', name='c_sid')

    def __repr__(self):
        return f'{self.sid} - {self.sname} - {self.rating} - {self.age}'


class Boat(db.Model):
    __tablename__ = 'boat'

    bid = db.Column(db.Integer, primary_key=True, nullable=False)
    bname = db.Column(db.String(40))
    color = db.Column(db.String(40))
    db.PrimaryKeyConstraint('bid', name='c_bid')

    def __repr__(self):
        return f'{self.bid} - {self.bname} - {self.color}'


class Marina(db.Model):
    __tablename__ = 'marina'

    mid = db.Column(db.Integer, primary_key=True, nullable=False)
    mname = db.Column(db.String(40), nullable=False)
    capacity = db.Column(db.Integer)
    db.PrimaryKeyConstraint('mid', name='c_mid')

    def __repr__(self):
        return f'{self.mid} - {self.mname} - {self.capacity}'


class Reservation(db.Model):
    __tablename__ = 'reservation'
    sid = db.Column(db.Integer, db.ForeignKey(
        'sailor.sid', ondelete="CASCADE"), primary_key=True, nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey(
        'boat.bid', ondelete="CASCADE"), primary_key=True, nullable=False)
    mid = db.Column(db.Integer, db.ForeignKey(
        'marina.mid', ondelete="SET NULL"))
    r_date = db.Column(db.String(12), primary_key=True, nullable=False)
    db.PrimaryKeyConstraint('sid', 'bid', 'r_date', name='p_key')

    def __repr__(self):
        return f'{self.sid} - {self.bid} - {self.mid} - {self.r_date}'


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
        reservation_data = {'sid': reservation.sid,
                            'bid': reservation.bid, 'mid': reservation.mid, 'r_date': reservation.r_date}
        output.append(reservation_data)

    return {'reservations': output}
