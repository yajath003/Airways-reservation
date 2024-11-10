from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, EmailField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Email
from flask_wtf.file import FileField
from werkzeug.security import check_password_hash
from admin.models import admin_login

class signupForm(FlaskForm):
    admin_name = StringField('admin Name', validators=[InputRequired()])
    email = EmailField('Email-ID', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    confirm_password = PasswordField('Repeat Password', validators=[EqualTo('password', message='Passwords must match')])

    def validate_admin_name(self, admin_name):
        admin = admin_login.query.filter_by(admin_name=admin_name.data).first()
        if admin:
            raise ValidationError('This adminname is already in use.')

    def validate_email(self, email):
        admin = admin_login.query.filter_by(email=email.data).first()
        if admin:
            raise ValidationError('This email is already in use.')

class loginForm(FlaskForm):
    admin_name = StringField('Admin Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Login')

    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators=extra_validators)
        if not valid:
            return False
        admin = admin_login.query.filter_by(admin_name=self.admin_name.data).first()
        if admin and check_password_hash(admin.password, self.password.data):
            return True
        else:
            self.password.errors.append('Incorrect admin name or password')
            return False


class SearchForm(FlaskForm):
    searched = StringField(validators=[InputRequired()])
    submit = SubmitField("Submit")


class FlightForm(FlaskForm):
    company = StringField('Company', validators=[InputRequired()])
    start_loc = StringField('Start location', validators=[InputRequired()])
    destination = StringField('Destination', validators=[InputRequired()])
    available_seats = IntegerField('Available seats', validators=[InputRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
