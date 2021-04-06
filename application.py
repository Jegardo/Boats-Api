from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data.db'
db = SQLAlchemy(app)


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class Sailor(db.Model):
    __tablename__ = 'sailor'

    sid = db.Column(db.Integer, primary_key=True, nullable=False)
    sname = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, db.CheckConstraint(
        '1 < rating < 10', name='c_rating'))
    age = db.Column(db.Integer, db.CheckConstraint('age > 17', name='c_age'))
    db.PrimaryKeyConstraint('sid', name='c_sid')

    reservations = relationship(
        "Reservation", cascade="all, delete, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f'{self.sid} - {self.sname} - {self.rating} - {self.age}'


class Boat(db.Model):
    __tablename__ = 'boat'

    bid = db.Column(db.Integer, primary_key=True, nullable=False)
    bname = db.Column(db.String(40))
    color = db.Column(db.String(40))
    db.PrimaryKeyConstraint('bid', name='c_bid')

    reservations = relationship(
        "Reservation", cascade="all, delete, delete-orphan", passive_deletes=True)

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

    rid = db.Column(db.Integer, primary_key=True, nullable=False)
    sid = db.Column(db.Integer, db.ForeignKey(
        'sailor.sid', ondelete="CASCADE"), nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey(
        'boat.bid', ondelete="CASCADE"), nullable=False)
    mid = db.Column(db.Integer, db.ForeignKey(
        'marina.mid', ondelete="SET NULL"))
    r_date = db.Column(db.String(12), nullable=False)
    db.PrimaryKeyConstraint('rid', name='c_rid')

    def __repr__(self):
        return f'{self.rid} - {self.sid} - {self.bid} - {self.mid} - {self.r_date}'


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


@app.route('/sailors/<id>')
def get_sailor(id):
    sailor = Sailor.query.get_or_404(id)
    return{'sid': sailor.sid, 'sname': sailor.sname,
           'rating': sailor.rating, 'age': sailor.age}


@app.route('/sailors', methods=['POST'])
def set_sailor():
    sailor = Sailor(sid=request.json['sid'], sname=request.json['sname'],
                    rating=request.json['rating'], age=request.json['age'])
    db.session.add(sailor)
    db.session.commit()
    return{'sid': sailor.sid, 'sname': sailor.sname}


@app.route('/sailors/<id>', methods=['DELETE'])
def delete_sailor(id):
    sailor = Sailor.query.get(id)
    if sailor is None:
        return {"error": "not found!"}
    db.session.delete(sailor)
    db.session.commit()
    return {"message": "deleted!"}


@app.route('/boats')
def get_boats():
    boats = Boat.query.all()

    output = []
    for boat in boats:
        boat_data = {'bid': boat.bid, 'bname': boat.bname, 'color': boat.color}
        output.append(boat_data)

    return {'boats': output}


@app.route('/boats/<id>')
def get_boat(id):
    boat = Boat.query.get_or_404(id)
    return {'bid': boat.bid, 'bname': boat.bname, 'color': boat.color}


@app.route('/boats', methods=['POST'])
def set_boat():
    boat = Boat(
        bid=request.json['bid'], bname=request.json['bname'], color=request.json['color'])
    db.session.add(boat)
    db.session.commit()
    return{'bid': boat.bid, 'bname': boat.bname}


@app.route('/boats/<id>', methods=['DELTE'])
def delete_boat(id):
    boat = Boat.query.get(id)
    if boat is None:
        return {"error": "not found!"}
    db.session.delete(boat)
    db.session.commit()
    return {"message": "deleted!"}

@app.route('/marinas')
def get_marinas():
    marinas = Marina.query.all()

    output = []
    for marina in marinas:
        marina_data = {'mid': marina.mid,
                       'mname': marina.mname, 'capacity': marina.capacity}
        output.append(marina_data)

    return {'marinas': output}


@app.route('/marinas/<id>')
def get_marina(id):
    marina = Marina.query.get_or_404(id)
    return{'mid': marina.mid,
           'mname': marina.mname, 'capacity': marina.capacity}


@app.route('/marinas', methods=['POST'])
def set_marina():
    marina = Marina(
        mid=request.json['mid'], mname=request.json['mname'], capacity=request.json['capacity'])
    db.session.add(marina)
    db.session.commit()
    return{'mid': marina.mid, 'mname': marina.mname}


@app.route('/marinas/<id>', methods=['DELETE'])
def delete_marina(id):
    marina = Marina.query.get(id)
    if marina is None:
        return {"error": "not found!"}
    db.session.delete(marina)
    db.session.commit()
    return{"message": "deleted!"}


@app.route('/reservations')
def get_reservations():
    reservations = Reservation.query.all()

    output = []
    for reservation in reservations:
        reservation_data = {'rid': reservation.rid, 'sid': reservation.sid,
                            'bid': reservation.bid, 'mid': reservation.mid, 'r_date': reservation.r_date}
        output.append(reservation_data)

    return {'reservations': output}


@app.route('/reservations/<id>')
def get_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    return{'rid': reservation.rid, 'sid': reservation.sid,
           'bid': reservation.bid, 'mid': reservation.mid, 'r_date': reservation.r_date}


@app.route('/reservations', methods=['POST'])
def set_reservation():
    reservation = Reservation(rid=request.json['rid'], sid=request.json['sid'],
                              bid=request.json['bid'], mid=request.json['mid'], r_date=request.json['r_date'])
    if Sailor.query.get(reservation.sid) is None:
        return {"Error": "Sailor doesn't exist!"}
    if Boat.query.get(reservation.bid) is None:
        return {"Error": "Boat doesn't exist!"}
    if Marina.query.get(reservation.mid) is None:
        return {"Error": "Marina doesn't exist!"}
    db.session.add(reservation)
    db.session.commit()

    return{'rid': reservation.rid, 'r_date': reservation.r_date}


@app.route('/reservations/<id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    if reservation is None:
        return {"error": "not found!"}
    db.session.delete(reservation)
    db.session.commit()
    return {"message": "deleted!"}