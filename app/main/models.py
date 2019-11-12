from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    Username = db.Column(db.String, primary_key=True, nullable = False)
    fullName = db.Column(db.String, nullable = False)
    passwordHash = db.Column(db.String, nullable = False)
    Email = db.Column(db.String, nullable = False)
    userStatus = db.Column(db.String) # are they a regular user, patient, or therapist

    journal = db.relationship("Journal", uselist=False, backref="Users")

    def add_journal(self, title):
        new_journal = Journal(title = title, UserID = self.Username)
        db.session.add(new_journal)
        db.session.commit()

    def become_Patient(self):
        new_patient = Patient(Username = self.Username, patientName = self.fullName) 
        db.session.add(new_patient)
        db.session.commit()

    def become_Therapist(self, therapistName):
        new_therapist = Therapist(therapistName = therapistName, Username = self.Username)
        #Users.userStatus = "Therapist"
        db.session.add(new_therapist)
        db.session.commit()

class Profile (db.Model):
    __tablename__ = "Profile"
    ProfileID = db.Column(db.Integer, db.ForeignKey('Users.Username'), primary_key=True )
    #MemberStatus = db.Column(db.String, db.ForeinKey('Users.userStatus'))

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

class Therapist(db.Model):
    __tablename__ = "Therapist"
    Username = db.Column(db.Integer, db.ForeignKey('Users.Username'), primary_key=True)
    therapistName = db.Column(db.String, db.ForeignKey('Users.fullName'))
    #TherapistID = db.Column(db.Integer, unique = True)
    #T_Patients_ID = db.Column(db.Integer, db.ForeignKey('T_Patients.T_ID'))
 
    #def add_patient(self, Username, patientName):
    #    new_assigned_patient = Patient(T_ID = self.TherapistID, P_ID = P_ID, patientName = patientName)

    patients = db.relationship("Patient", backref = "Therapist")

#class T_Patients(db.Model):
#    __tablename__ = "T_Patients"
#    T_ID = db.Column(db.Integer, db.ForeignKey ('Therapist.TherapistID'), primary_key = True)
#    P_ID = db.Column(db.Integer, db.ForeignKey('Patient.PatientID'), primary_key = True)
#    patientName = db.Column(db.String, db.ForeignKey('Patient.patientName'))

class Patient(db.Model):
    __tablename__ = "Patient"
    Username = db.Column(db.String, db.ForeignKey('Users.Username'), primary_key=True)
    #insuranceProvider = db.Column(db.String)
    patientName = db.Column(db.String, db.ForeignKey('Users.fullName'))
    TherapistID = db.Column(db.Integer, db.ForeignKey('Therapist.Username'), unique = True)
    #T_ID = db.Column(db.Integer, db.ForeignKey ('Therapist.TherapistID')
