from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from user.forms import loginForm, signupForm, SearchForm, BookingForm
from user.models import user_login, BookingModel
from admin.models import flights
from application import db

user_app = Blueprint('user_app', __name__)

@user_app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = loginForm()
    if form.validate_on_submit():
        req = user_login.query.filter_by(user_name=form.user_name.data).first()
        if req:
            session['user_id'] = req.user_id
            session['user_name'] = form.user_name.data
            return redirect(url_for('user_app.home'))
    return render_template('user/signin.html', form=form)

@user_app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = signupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = user_login(
            user_name=form.user_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.sign_in'))
    return render_template('user/signup.html', form=form)


@user_app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        session['search'] = form.searched.data
        return redirect(url_for('.search'))

    flights_list = flights.query.all()
    return render_template('user/home.html', form=form, flight=flights_list)


@user_app.route('/search', methods=['GET', 'POST'])
def search():
    search_value = session.get('search')
    planes = []
    if search_value:
        planes = flights.query.filter(
            (flights.flight_id.ilike(f'%{search_value}%')) |
            (flights.company.ilike(f'%{search_value}%')) |
            (flights.start_loc.ilike(f'%{search_value}%')) |
            (flights.destination.ilike(f'%{search_value}%')) |
            (flights.price.ilike(f'%{search_value}%'))
        ).all()
        if planes:
            flash('Yay! Something was found!')
        else:
            flash('No search results found.')

    return render_template('user/search.html', flight=planes)


@user_app.route('/flightdetails', methods=['GET', 'POST'])
def flightdetails():
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
    return render_template('user/flight_details.html', plane=details)


@user_app.route('/booking/<int:flight_id>', methods=['GET', 'POST'])
def booking(flight_id):
    form = BookingForm()
    plane = flights.query.filter_by(flight_id=flight_id).first()
    if not plane:
        flash("Flight not found.")
        return redirect(url_for('.home'))
    if form.validate_on_submit():
        selected = form.seats.data
        if plane.available_seats >= selected:
            new_booking = BookingModel(
                seats_selected=selected,
                user_id=session.get('user_id'),
                flight_id=flight_id
            )
            plane.available_seats -= selected
            db.session.add(new_booking)
            db.session.commit()
            flash('Selected seats booked successfully...')
            return redirect(url_for('.home'))
        else:
            flash('The selected seats are not available...')
    return render_template('user/booking.html', flight_id=flight_id, plane=plane, form=form)


@user_app.route('/proffile', methods=['GET', 'POST'])
def proffile():
    user = user_login.query.filter_by(user_id=session.get('user_id')).first()
    booking_table = BookingModel.query.filter_by(user_id=session.get('user_id')).all()
    dic = {
        'flight_id': [],
        'From': [],
        'To': [],
        'Seats': [],
        'company': []
    }
    for booking in booking_table:
        dic['flight_id'].append(booking.flight_id)
        dic['Seats'].append(booking.seats_selected)

    for flight_id in dic['flight_id']:
        flight = flights.query.filter_by(flight_id=flight_id).first()
        if flight:
            dic['From'].append(flight.start_loc)
            dic['To'].append(flight.destination)
            dic['company'].append(flight.company)
    return render_template('user/profile.html', user=user, booking_table=dic)
