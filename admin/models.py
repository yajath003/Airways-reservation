from application import db

class admin_login(db.Model):
    __tablename__ = 'admin_login'
    admin_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    admin_name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)


class flights(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    company = db.Column(db.String(80), nullable=False)
    start_loc = db.Column(db.String(80), nullable=False)
    destination = db.Column(db.String(80), nullable=False)
    available_seats = db.Column(db.Integer,  nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.String(80), db.ForeignKey('admin_login.admin_id'), nullable=False)