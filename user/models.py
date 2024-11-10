from application import db
from admin.models import flights

class user_login(db.Model):
    __tablename__ = 'user_login'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)


class BookingModel(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    seats_selected = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_login.user_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False, )
