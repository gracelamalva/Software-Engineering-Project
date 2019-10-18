from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    Username = db.Column(db.Integer, primary_key=True, nullable = False)
    fullName = db.Column(db.varchar(45), nullable = False)
    passwordHash = db.Column(db.varchar(11), nullable = False)
    Email = db.Column(db.varchar(45), nullable = False)

class Journal(db.Model):
    __tablename__ = "Journal"
    JournalID = db.Column(db.Integer, primary_key=True, nullable = False)
    UserID = db.Column(db.varchar(30), db.ForeignKey('Users.Username'), nullable = False)

class JournalEntry(db.Model):
    __tablename__ = "JournalEntry"
    EntryID = db.Column(db.Integer, primary_key=True, nullable = False)
    EntryTitle = db.Column(db.varchar(30))
    EntryText = db.Column(db.longtext)
    Date_Time = db.Column(db.datetime)
    J_ID = db.Column(db.Integer, db.ForeignKey('Journal.JournalID'), nullable = False)

