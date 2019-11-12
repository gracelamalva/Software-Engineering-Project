from flask_sqlalchemy import SQLAlchemy
#from .import db
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    Username = db.Column(db.String, primary_key=True, nullable = False)
    fullName = db.Column(db.String, nullable = False)
    passwordHash = db.Column(db.String, nullable = False)
    Email = db.Column(db.String, nullable = False)

    journal = db.relationship("Journal", uselist=False, backref="Users")

    def add_journal(self, title):
        new_journal = Journal(title = title, UserID = self.Username)
        db.session.add(new_journal)
        db.session.commit()

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
    UserID = db.Column(db.String, db.ForeignKey('Users.Username'), nullable = False)
    
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
    EntryEmotion = db.Column(db.String)
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
""" 
class Affirmation(db.Model):
    __tablename__ = "Affirmation"
    AffirmationID = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    Affirmationtitle = db.Column(db.String, nullable=False)
    AffirmationUserID = db.Column(db.String, db.ForeignKey('Users.Username'), nullable=False)

    Affirmationentries = db.relationship("AffirmationEntry", backref="Affirmation")

    def add_Affirmationentry(self, Affirmationentrytitle, Affirmationentrytext):
        new_Affirmationentry = AffirmationEntry(EntryTitle=Affirmationentrytitle, EntryText=Affirmationentrytext, A_ID=self.AffirmationID)
        db.session.add(new_Affirmationentry)
        db.session.commit()

class AffirmationEntry(db.Model):
    __tablename__ = "AffirmationEntry"
    AffirmationEntryID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    AffirmationEntryTitle = db.Column(db.String)
    AffirmationEntryText = db.Column(db.String)
    #A_ID = db.Column(db.Integer, db.ForeignKey('Affirmation.AffirmationID'), nullable=False)
"""

#class AnalyzedEntry(db.Model):
#    __tablename__ = "AnalyzedJournalEntry"
#    AnalyzedEntryID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
#    EntryEmotion = db.Column(db.String, nullable =False)
#    E_ID = db.Column(db.Integer, db.ForeignKey('JournalEntry.EntryID'))