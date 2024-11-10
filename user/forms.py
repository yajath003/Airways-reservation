from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, EmailField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Email
from flask_wtf.file import FileField
from werkzeug.security import check_password_hash

from user.models import user_login

class signupForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired()])
    email = EmailField('Email-ID', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    confirm_password = PasswordField('Repeat Password', validators=[EqualTo('password', message='Passwords must match')])

    def validate_user_name(self, user_name):
        user = user_login.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('This username is already in use.')

    def validate_email(self, email):
        user = user_login.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use.')

class loginForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Login')

    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators=extra_validators)
        if not valid:
            return False
        user = user_login.query.filter_by(user_name=self.user_name.data).first()
        if user and check_password_hash(user.password, self.password.data):
            return True
        else:
            self.password.errors.append('Incorrect username or password')
            return False

class SearchForm(FlaskForm):
    searched = StringField(validators=[InputRequired()])
    submit = SubmitField("Submit")


class BookingForm(FlaskForm):
    seats = IntegerField("Selected seats", validators=[InputRequired()])
    submit = SubmitField("Submit")