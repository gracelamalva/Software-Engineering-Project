from flask_sqlalchemy import SQLAlchemy
from app import db
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    Username = db.Column(db.Integer, primary_key=True, nullable=False)
    fullName = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)

    journal = db.relationship("Journal", uselist=False, backref="Users")

    def add_journal(self, title):
<<<<<<< HEAD
        new_journal = Journal(title = title, UserID = self.Username)
=======
        new_journal = Journal(title=title, J_ID=self.Username)
>>>>>>> b4d921013aa4bdd469e789ae2a7ffc800d142ee2
        db.session.add(new_journal)
        db.session.commit()


class Journal(db.Model):
    __tablename__ = "Journal"
<<<<<<< HEAD
    JournalID = db.Column(db.Integer, primary_key=True, nullable = False) 
    title = db.Column(db.String, nullable = False)
    UserID = db.Column(db.String, db.ForeignKey('Users.Username'), nullable = False)
    
    entries = db.relationship("JournalEntry", backref = "Journal")
=======
    JournalID = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    UserID = db.Column(db.String, db.ForeignKey('Users.Username'), nullable=False)

    entries = db.relationship("JournalEntry", back_populates="Journal")
>>>>>>> b4d921013aa4bdd469e789ae2a7ffc800d142ee2

    def add_entry(self, entrytitle, entrytext, date_time):
        new_entry = JournalEntry(Entrytitle=entrytitle, EntryText=entrytext, Date_Time=date_time, J_ID=self.JournalID)
        db.session.add(new_entry)
        db.session.commit()


class JournalEntry(db.Model):
    __tablename__ = "JournalEntry"
    EntryID = db.Column(db.Integer, primary_key=True, nullable=False)
    EntryTitle = db.Column(db.String)
    EntryText = db.Column(db.String)
    Date_Time = db.Column(db.DateTime)
    J_ID = db.Column(db.Integer, db.ForeignKey('Journal.JournalID'), nullable=False)
