from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from admin.models import admin_login, flights
from admin.forms import loginForm, signupForm, FlightForm, SearchForm
from application import db

admin_app = Blueprint('admin_app', __name__)

@admin_app.route('/')
def index():
    return render_template('index.html')

@admin_app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = loginForm()
    if form.validate_on_submit():
        req = admin_login.query.filter_by(admin_name=form.admin_name.data).first()
        if req:
            session['admin_id'] = req.admin_id
            session['admin_name'] = form.admin_name.data
            return redirect(url_for('admin_app.hoome'))
    return render_template('admin/signin.html', form=form)

@admin_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        admin = admin_login(
            admin_name=form.admin_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('.signin'))
    return render_template('admin/signup.html', form=form)


@admin_app.route('/hoome', methods = ['GET', 'POST'])
def hoome():
    form = SearchForm()
    if request.method == 'POST':
        value = request.form.get('searched')
        session['search'] = value
        return redirect(url_for('.searchh'))
    flight = flights.query.all()
    return render_template('admin/home.html', form=form, flight=flight)


@admin_app.route('/new_flight', methods = ['GET', 'POST'])
def new_flight():
    form = FlightForm()
    if form.validate_on_submit():
        flight = flights(
            company=form.company.data,
            start_loc=form.start_loc.data,
            destination=form.destination.data,
            available_seats=form.available_seats.data,
            price=form.price.data,
            total_seats=form.available_seats.data,
            admin_id=session['admin_id']
        )
        db.session.add(flight)
        db.session.commit()
        flash('New flight added...!')
        return redirect(url_for('.hoome'))
    return render_template('admin/new_flight.html', form=form)


@admin_app.route('/dlt_flight', methods = ['GET', 'POST'])
def dlt_flight():
    if request.method == 'POST':
        flight_ids = request.form.getlist('flight_ids')
        for flight in flight_ids:
            planes = flights.query.filter_by(flight_id=flight)
            for plane in planes:
                db.session.delete(plane)
        db.session.commit()
        flash('The selected Flights deleted successfully')
        return redirect(url_for('admin_app.dlt_flight'))
    flightss = flights.query.all()
    return render_template('admin/dlt_flight.html', flights=flightss)


@admin_app.route('/searchh', methods=['GET', 'POST'])
def searchh():
    search_value = session.get('search')
    if search_value:
        planes = (flights.query.filter(flights.flight_id.ilike(f'%{search_value}%')).all()
                   or flights.query.filter(flights.company.ilike(f'%{search_value}%')).all()
                   or flights.query.filter(flights.start_loc.ilike(f'%{search_value}%')).all()
                   or flights.query.filter(flights.destination.ilike(f'%{search_value}%')).all()
                   or flights.query.filter(flights.price.ilike(f'%{search_value}%')).all())
        if planes:
            flash('yaay something found...!')
        else:
            flash('No search results')
    return render_template('admin/search.html', flight=planes)


@admin_app.route('/flight_details', methods=['GET', 'POST'])
def flight_details():
    if request.method == 'POST':
        session['flight_id'] = request.form.get('flight_id')
    else:
        flight_id = request.args.get('flight_id')
        if flight_id:
            session['flight_id'] = flight_id

    flight_id = session.get('flight_id')
    if not flight_id:
        return "flight ID not found", 400

    details = flights.query.filter_by(flight_id=flight_id).first()
    if not details:
        return "flight not found", 404
    return render_template('admin/flight_details.html', plane=details)


@admin_app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = admin_login.query.filter_by(admin_id=session.get('admin_id')).first()
    return render_template('admin/profile.html', user=user)