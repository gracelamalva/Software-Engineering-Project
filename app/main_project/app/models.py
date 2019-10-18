from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    Username = db.Column(db.Integer, primary_key=True, nullable = False)
    fullName = db.Column(db.varchar(45), nullable = False)
    passwordHash = db.Column(db.varchar(11), nullable = False)
    Email = db.Column(db.varchar(45), nullable = False)

    journal = relationship("Journal", uselist=False, back_populates="Users")


    def add_journal(self, title):
        new_journal = Journal(title = title, J_ID = self.Username)
        db.session.add(new_journal)
        db.session.commit()
    

class Journal(db.Model):
    __tablename__ = "Journal"
    JournalID = db.Column(db.Integer, primary_key=True, nullable = False) 
    title = db.Column(db.varchar(30), nullable = False)
    UserID = db.Column(db.varchar(30), db.ForeignKey('Users.Username'), nullable = False)
    
    entries = relationship("JournalEntry", back_populates = "Journal")
    
    def add_entry(self, entrytitle, entrytext, date_time):
        new_entry = JournalEntry(Entrytitle = entrytitle, EntryText = entrytext, Date_Time = date_time, J_ID = self.JournalID)
        db.session.add(new_entry)
        db.session.commit()

class JournalEntry(db.Model):
    __tablename__ = "JournalEntry"
    EntryID = db.Column(db.Integer, primary_key=True, nullable = False)
    EntryTitle = db.Column(db.varchar(30))
    EntryText = db.Column(db.longtext)
    Date_Time = db.Column(db.datetime)
    J_ID = db.Column(db.Integer, db.ForeignKey('Journal.JournalID'), nullable = False)

