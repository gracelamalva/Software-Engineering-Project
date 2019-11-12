from flask_wtf import FlaskForm
from wtforms import (
    DateField, StringField, TextAreaField,
    SelectMultipleField, SubmitField,
    PasswordField, BooleanField,
    DateTimeField, IntegerField, FloatField, FileField, SelectField)
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from .models import Users, AffirmationEntry
#from . import db

class createAEntry(FlaskForm):
    EntryTitle = StringField('Affirmation Entry Title', validators=[DataRequired()])
    EntryText = StringField('Affirmation Entry Text', validators=[DataRequired()])
    submit = SubmitField('Create')