from . import flask_bcrypt
from . import login
from datetime import datetime
from hashlib import md5
from . import db
from flask_sqlalchemy import SQLAlchemy
#from .import db


db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String, unique=True, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    userstatus = db.Column(db.String, default = "User")

    journal = db.relationship("Journal", uselist=False, backref='Users')

    def add_journal(self, title):
        new_journal = Journal(title = title, UserID = self.Username)
        db.session.add(new_journal)
        db.session.commit()
    
    def become_Patient(self):
        new_patient = Patient(id = self.id, patientName = self.fullname)
        db.session.add(new_patient)
        db.session.commit()
    
    def become_Therapist(self):
        new_therapist = Therapist(id = self.id, therapistName = self.fullname)
        db.session.add(new_therapist)
        db.session.commit()

    @property
    def password(self):
        return 'hashed password'

    @password.setter
    def password(self, pw):
        self.password_hash = flask_bcrypt.generate_password_hash(pw).decode('utf-8')

    def check_password(self, pw):
        return flask_bcrypt.check_password_hash(self.password_hash, password=pw)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True


@login.user_loader
def load_user(id):
    if isinstance(id, int):
        pass
    elif isinstance(id, int):
        if id.strip().isdigit():
            id = int(id)
        else:
            return
    else:
        return
    return Users.query.get(id)

    #T_ID = db.Column(db.Integer, db.ForeignKey ('Therapist.TherapistID')
#class User(db.Model):
#    __tablename__ = "User"
#    Username = db.Column(db.String, primary_key=True, nullable = False)
#    fullName = db.Column(db.String, nullable = False)
#    passwordHash = db.Column(db.String, nullable = False)
#    Email = db.Column(db.String, nullable = False)
#
#    journal = db.relationship("Journal", uselist=False, backref="User")

"""
    def add_affirmation(self,title):
        new_affirmation=Affirmation(title = title, UserID = self.Username)
        db.session.add(new_affirmation)
        db.session.commit()
"""
class Journal(db.Model):
    __tablename__ = "Journal"
    JournalID = db.Column(db.Integer, primary_key=True, unique = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    UserID = db.Column(db.String, db.ForeignKey('Users.id'), nullable = False)

    entries = db.relationship("JournalEntry", backref="Journal")

    def add_entry(self, entrytitle, entrytext, date_time):
        new_entry = JournalEntry(EntryTitle = entrytitle, EntryText = entrytext, Date_Time = date_time, J_ID = self.JournalID)
        db.session.add(new_entry)
        db.session.commit()

class JournalEntry(db.Model):
    __tablename__ = "JournalEntry"
    EntryID = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement = True)
    EntryTitle = db.Column(db.String)
    EntryText = db.Column(db.String)
    Date_Time = db.Column(db.DateTime, nullable = False)
    #EntryEmotion = db.Column(db.Integer, db.ForeignKey('Journal.JournalID'), nullable=False)
    J_ID = db.Column(db.Integer, db.ForeignKey('Journal.JournalID'), nullable = False)

class AffirmationEntry(db.Model):
    __tablename__ = "AffirmationEntry"
    AffirmationEntryID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    AffirmationEntryTitle = db.Column(db.String)
    AffirmationEntryText = db.Column(db.String)
    #User_ID = db.Column(db.String, db.ForeignKey('Users.id'), nullable = False)

    def add_AEntry(self, aTitle, aText):
        new_AffirmationEntry = AffirmationEntry(AffirmationEntryTitle=aTitle, AffirmationEntryText=aText)
        db.session.add(new_AffirmationEntry)
        db.session.commit()


class Therapist(db.Model):
    __tablename__ = "Therapist"
    id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    therapistName = db.Column(db.String, db.ForeignKey('Users.fullname'))
    TherapistID = db.Column(db.String, db.ForeignKey('Therapist.id'), unique = True)

    myPatients = db.relationship("Patient", backref = "Therapist")


class Patient(db.Model):
    __tablename__ = "Patient"
    id = db.Column(db.String, db.ForeignKey('Users.id'), primary_key=True)
    #insuranceProvider = db.Column(db.String)
    patientName = db.Column(db.String, db.ForeignKey('Users.fullname'))
    T_ID = db.Column(db.Integer, db.ForeignKey ('Therapist.TherapistID'))

    