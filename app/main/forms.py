from flask_wtf import FlaskForm
from wtforms import (
    DateField, StringField, TextAreaField,
    SelectMultipleField, SubmitField,
    PasswordField, BooleanField,
    DateTimeField, IntegerField, FloatField, FileField, SelectField)
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from .models import Users, AffirmationEntry
from . import db

from dateutil.tz import tz, tzlocal, tzutc

class RegisterForm(FlaskForm):
    Username = StringField('UserName', validators=[DataRequired()])
    fullname = StringField('FullName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, max=32, message='The length of a password should be between 6 and 32')])
    password2 = PasswordField(
        'Password Repeat', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_name(self, Username):
        super()
        user = Users.query.filter_by(Username=Username.data).first()
        if user is not None:
            raise ValidationError('This username has been taken')

    def validate_email(self, email):
        super()
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email has been taken')


class LoginForm(FlaskForm):
    Username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, max=32, message='The length of a password should be between 6 and 32')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[
        DataRequired(), Length(6, max=32, message='The length of a password should be between 6 and 32')])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), Length(6, max=32, message='The length of a password should be between 6 and 32')])

    submit = SubmitField('Submit')

    def validate_old_password(self, old_password):
        user = Users.query.get(current_user.id)
        if user is None:
            print(user)
            return
        if not user.check_password(old_password.data):
            return ValidationError(message='Invalid Old Password.')

class UpdateAccountInfo(FlaskForm):
    Username = StringField('New Usermame', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_name(self, Username):
        if Username.data != current_user.Username:
            user = Users.query.filter_by(Username=Username.data).first()
        if user is not None:
            raise ValidationError('Username already exists! Choose a different one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists! Choose a different one!')

class createAEntry(FlaskForm):
    EntryTitle = StringField('Affirmation Entry Title', validators=[DataRequired()])
    EntryText = StringField('Affirmation Entry Text', validators=[DataRequired()])
    submit = SubmitField('Create')
