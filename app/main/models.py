from . import flask_bcrypt
from . import login
from datetime import datetime
from . import db


#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now)

    is_active = db.Column(db.Boolean, default=True)

    journals = db.relationship("Journal", backref='User', passive_deletes=True)

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
    elif isinstance(id, str):
        if id.strip().isdigit():
            id = int(id)
        else:
            return
    else:
        return
    return User.query.get(id)


#class User(db.Model):
#    __tablename__ = "User"
#    Username = db.Column(db.String, primary_key=True, nullable = False)
#    fullName = db.Column(db.String, nullable = False)
#    passwordHash = db.Column(db.String, nullable = False)
#    Email = db.Column(db.String, nullable = False)
#
#    journal = db.relationship("Journal", uselist=False, backref="User")
#
#    def add_journal(self, title):
#        new_journal = Journal(title = title, UserID = self.Username)
#        db.session.add(new_journal)
#        db.session.commit()

class Journal(db.Model):
    __tablename__ = "Journal"
    JournalID = db.Column(db.Integer, primary_key=True, unique = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    UserID = db.Column(db.String, db.ForeignKey('User.name'), nullable = False)

    entries = db.relationship("JournalEntry", backref = "Journal")

    def add_entry(self, entrytitle, entrytext, date_time):
        new_entry = JournalEntry(EntryTitle = entrytitle, EntryText = entrytext, Date_Time = date_time, J_ID = self.JournalID)
        db.session.add(new_entry)
        db.session.commit()

class JournalEntry(db.Model):
    __tablename__ = "JournalEntry"
    EntryID = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement = True)
    EntryTitle = db.Column(db.String)
    EntryText = db.Column(db.String)
    Date_Time = db.Column(db.DateTime)
    J_ID = db.Column(db.Integer, db.ForeignKey('Journal.JournalID'), nullable = False)


#class AnalyzedEntry(db.Model):
#    __tablename__ = "AnalyzedJournalEntry"
#    AnalyzedEntryID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
#    EntryEmotion = db.Column(db.String, nullable =False)
#    E_ID = db.Column(db.Integer, db.ForeignKey('JournalEntry.EntryID'))
