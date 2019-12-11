import sys, csv, os, datetime
from datetime import timedelta

from bin.ud.conll17_ud_eval import HEAD
from werkzeug.urls import url_parse
from app.main import bp, models, mail
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify, flash
from app.main.models import *
from .models import Users
from .models import Journal
from .models import JournalEntry
from .models import AffirmationEntry
from flask_sqlalchemy import SQLAlchemy
# from app.api.request import *
from app.api.request import analyze
from flask_login import login_required, current_user, logout_user, login_user
from .forms import RegisterForm, LoginForm, ChangePasswordForm, UpdateAccountInfo, createAEntry, HelpDeskForm
from flask_mail import Message, Mail


from .forms import RegisterForm, LoginForm, ChangePasswordForm, UpdateAccountInfo, createAEntry
from flask import send_file
from flask import Response


#import chatbot files
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import spacy
nlp = spacy.load('en_core_web_sm')

@bp.route('/', methods=['GET','POST'])
def index():
    user = current_user

    return render_template('index.html', user = user)

@bp.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()

    if form.validate_on_submit():

        user = models.Users(
            Username=form.Username.data, email=form.email.data, fullname=form.fullname.data
            )
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your acc created. Please login with your new credential.', category='success')
        return redirect(url_for('main.login'))
    return render_template('user_register.html', title='User Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(Username=form.Username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('UserName or Password was Wrong', category='danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('user_login.html', title='User Login', form=form)

@bp.route('/update', methods=['POST', 'GET'])
@login_required
def update():
    form = UpdateAccountInfo()

    if form.validate_on_submit():
        current_user.Username = form.Username.data
        current_user.email = form.email.data
        db.session.merge(current_user)
        db.session.commit()
        flash('Your changes have been saved!', category='success')
        return redirect(url_for('main.account'))

    elif request.method == 'GET':
        form.Username.data = current_user.Username
        form.email.data = current_user.email
    return render_template('user_update.html', form=form)

@bp.route('/viewAccount')
@login_required
def accountview():
    #user = current_user
    requests = Request.query.filter_by(to = current_user.id)
    me = Patient.query.get(current_user.id)
    patient = Patient.query.get(current_user.id)
    mytherapist = 0

    if current_user.userstatus == "Patient":
        me = Patient.query.get(current_user.id)
        requests = Request.query.filter_by(to = current_user.id)
        patients = Patient.query.join(T_Patients, Patient.id == T_Patients.p_id).filter(T_Patients.t_id == current_user.id).all()
        #requests = Request.query.filter_by(to = current_user.id)
        #therapist = T_Patients.query.filter_by(p_id = current_user.id)
        mytherapist = me.T_ID#Patient.query.filter_by(T_ID = me.T_ID)
        print(me.T_ID)
        print (patients, requests)
        return render_template('accountview.html', requests = requests, mytherapist = mytherapist, me = me, patients = patients)
  
    if current_user.userstatus == "Therapist":
        me = Therapist.query.get(current_user.id)
        requests = Request.query.filter_by(to = current_user.id)
        mypatients = T_Patients.query.filter_by(t_id = current_user.id)
        patients = Patient.query.join(T_Patients, Patient.id == T_Patients.p_id).filter(T_Patients.t_id == current_user.id).all()
        mytherapist = T_Patients.query.filter_by(p_id = 0)
        patient = Patient.query.get(0)


        #return render_template('accountview.html', requests = requests, patients = patients)
        return render_template('accountview.html', requests = requests, me = me, mytherapist = mytherapist, patient = patient, patients = patients)
    
    #print (patient, patients, requests)
    
    return render_template('accountview.html', requests = requests, mytherapist = mytherapist) #, patient = patient, patients = patients, me = me)

@bp.route('/reset', methods=['post', 'get'])
@login_required
def reset():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = models.Users.query.get(current_user.id)
        if user is None:
            os.abort(404)
        if not user.check_password(form.old_password.data):
            flash(message='Old password was invalid', category='warning')
        else:
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash(message='Password updated. Login with new password next time', category='success')

    return render_template('user_reset.html', form=form)

@bp.route('/deleteU/<int:id>', methods=['POST', 'DELETE'])
@login_required
def delete_user(id):
    user = models.Users.query.get(id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('Your Account Has Been Deleted!', category='success')
        return redirect(url_for('main.index'))
    return render_template('accountview.html', id=id)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/journal', methods = ['GET', 'POST'])
def journal():
    
    entries = JournalEntry.query.all()
    return render_template('journal.html', journal = journal, entries=entries)

@bp.route('/journal/downloadcsv', methods = ['GET', 'POST'])
def journal_downloadcsv():
    # entry = request.form.get("entry")
    entries = JournalEntry.query.all()
    csvLines = []
    # csv header
    csvLines.append("ID,Title,Text,DateTime")
    for entry in entries:
        # in order to escape double quotes, we should double the double quotes
        csvLine = []
        # ID
        csvLine.append("\"" + str(entry.EntryID).replace("\"", "\"\"") + "\"")
        # Title
        csvLine.append("\"" + entry.EntryTitle.replace("\"", "\"\"") + "\"")
        # Text
        csvLine.append("\"" + entry.EntryText.replace("\"", "\"\"") + "\"")
        # DateTime
        csvLine.append("\"" + str(entry.Date_Time).replace("\"", "\"\"") + "\"")

        csvLines.append(",".join(csvLine))

    return Response("\n".join(csvLines),
                    mimetype="text/csv",
                    headers={
                        "Content-Disposition":
                            "attachment;filename=entries.csv"
                    })

@bp.route('/search', methods=['GET', 'POST'])
def search():
    dt = request.args.get("date")
    ft = '%Y-%m-%d'
    date = datetime.strptime(dt, ft)
    entries = JournalEntry.query.filter(JournalEntry.Date_Time.between(date, date + timedelta(days=1))).all()
    return render_template('search.html', entries=entries)

@bp.route('/createjournal', methods=['POST', 'GET'])
def create_journal():
    #/<string:id>
    title = request.form.get("title")
    journal = Journal(title=title, UserID=current_user.id)
    db.session.add(journal)
    db.session.commit()

    journal=Journal.query.all()

    return render_template('journal.html', journal=journal)

@bp.route('/edit/<int:EntryID>', methods=['GET', 'POST', 'PUT'])
def edit(EntryID):
    entry = JournalEntry.query.get(EntryID)
    entries = JournalEntry.query.filter_by(EntryID=EntryID)
    entries = JournalEntry.query.all()
    if (request.method == "POST"):
        entry.EntryTitle = request.form.get("newtitle")
        entry.EntryText = request.form.get("newtext")

    #entries = JournalEntry.query.all()

        return render_template('journal.html', entries=entries)

    return render_template('edit.html', entries=entries)

@bp.route('/add/<int:JournalID>', methods=['GET', 'POST'])
def add(JournalID):
    journal = Journal.query.get(JournalID)

    if request.method == "POST":
        # journal =Journal.query.get(JournalID)
        entrytitle = request.form.get("title")
        entrytext = request.form.get("entry")
        dt = request.form.get("date-time")
        ft = '%Y-%m-%dT%H:%M'
        result = datetime.strptime(dt, ft)

        journal.add_entry(entrytitle, entrytext, result)

    entries = JournalEntry.query.all()
    return render_template('journal.html', journal=journal, entries=entries)

@bp.route('/delete/<int:EntryID>', methods=['POST', 'GET', 'DELETE'])
def delete(EntryID):
    #entry = JournalEntry.query.get(EntryID)

    entry = JournalEntry.query.filter_by(EntryID = EntryID).first()

    db.session.delete(entry)
    db.session.commit()
    entries = JournalEntry.query.all()

    return render_template('journal.html', entries=entries)
    entry = JournalEntry.query.get(EntryID)

@bp.route('/analyze/<int:EntryID>', methods = ['GET', 'POST'])
def analyze_entry(EntryID):

    emotion = ""
    entry = JournalEntry.query.get(EntryID)

    if (request.method == "POST"):
        emotion = analyze(entry.EntryText)

        entry.EntryEmotion = emotion
        db.session.commit()

    entries = JournalEntry.query.all()

    return render_template('journal.html', entries=entries)

@bp.route('/analyze', methods = ['GET', 'POST'])
def analyze_text():

    analyzed_text = ""
    text = request.form['entry']

    if (request.method == "POST"):
        analyzed_text = analyze(text)

    return render_template('analyze.html', analyzed_text=analyzed_text, text=text)

@bp.route('/populate', methods=['GET', 'POST'])
def populate():
    query = db.insert(Users).values(Username="glamalva", fullName='grace', passwordHash="dfsfs34",  Email="gracegmailcom")
    # db.session.execute( "INSERT INTO Users (Username, fullName, passwordHash, Email) VALUES ('glamalva', 'gracelamalva', 'adfa43', 'glamalvagmailcom')")
    analyzed_text =  analyze(text)

    return render_template('analyze.html', analyzed_text = analyzed_text, text = text)

@bp.route('/dummyprofile/<string:Username>', methods = ['GET','POST'])
def profile(Username):

    user = Users.query.get(Username)

    if (request.method == "POST"):
        return render_template(url_for('patient'))

    if (user.userStatus == "Patient"):
         return render_template(url_for('patient'))

    return render_template('dummyprofile.html', user = user)

@bp.route('/patient' , methods = ['GET', 'POST'])
def patient():

    if current_user.userstatus == "Patient":
        flash('you cannot become a patient again')
        render_template('accountview.html')

    #user = Users.query.get(Username)
    user = current_user

    user.become_Patient()
    current_user.userstatus = "Patient"
    db.session.commit()

    user = current_user

    return render_template('accountview.html', user = user)

@bp.route('/therapist' , methods = ['GET', 'POST'])
def therapist():

    user = current_user

    user.become_Therapist()
    current_user.userstatus = "Therapist"
    db.session.commit()

    user = current_user
    return render_template('accountview.html', user = user)

@bp.route('/account')
@login_required
def account():

    #user = Users.query.filter(id)
    
    user = current_user
    flag = 0

    return render_template('account.html', user = user)

@bp.route('/findtherapist')
@login_required
def findtherapist():
    #user = current_user
    #requests = Request.query.filter_by(to = current_user.id)
    #patient = Patient.query.get(id = current_user.id)
    therapists= Therapist.query.all()
    #therapists = Therapist.query.filter_by(numPatients< 10, request.to != therapist.id)
    therapists = Therapist.query.join(Request, Therapist.id == Request.origin).filter(Therapist.numPatients < 10 , Request.to != current_user.id)

    return render_template('findtherapist.html',  therapists = therapists)#, availables = availables)

@bp.route('/findpatient')
@login_required
def findpatient():

    patients = Patient.query.all()
    requests = Request.query.filter_by(to = current_user.id)
    
    if (requests):
        print(requests)
   
        patients = Patient.query.join(Request, Patient.id == Request.origin).filter(Patient.hasTherapist == False, Request.to != current_user.id).all()
        #print(availables, current_user.id)

        return render_template('findpatient.html', patients = patients, requests = requests)#, availables = availables)
    
    return render_template('findpatient.html', patients = patients, requests = requests)


@bp.route('/revertaccount')
@login_required
def revertaccount():
    id = current_user.id
    user = current_user
    if current_user.userstatus == "Patient":
        patient = Patient.query.get(id)
        db.session.delete(patient)
    if current_user.userstatus == "Therapist":
        therapist = Therapist.query.get(id)
        db.session.delete(therapist)
    current_user.userstatus = "User"
    db.session.commit()

    return render_template('revertaccount.html')

@bp.route('/sendrequest/<int:to>')
@login_required
def sendrequest(to):

    id = current_user.id
    user = current_user

    if current_user.userstatus == "Therapist":
        therapist = Therapist.query.get(id)
        patient = Patient.query.get(to)
        request = Request(origin = therapist.id, to = patient.id)
        db.session.add(request)
        db.session.commit()

    if current_user.userstatus == "Patient":
        patient = Patient.query.get(id)
        therapist = Therapist.query.get(to)
        request = Request(origin = patient.id, to = therapist.id)
        db.session.add(request)
        db.session.commit()


    flash('Your request has been sent')

    return render_template('accountview.html')


@bp.route('/accept/<int:id>/<int:origin>')
@login_required
def accept(id,origin):

    request = Request.query.get(id)
    #origin = Request.query.get(origin)

    id = current_user.id
    user = current_user

    if current_user.userstatus == "Therapist":

        accepted_request = T_Patients(id = request.id, t_id = current_user.id , p_id = request.origin, response = "accepted")
        therapist = Therapist.query.get(current_user.id)
        therapist.numPatients += 1
        patient = Patient.query.get(request.origin)
        patient.hasTherapist = True
        patient.T_ID = therapist.therapistName
        db.session.add(accepted_request)
        db.session.commit()

    if current_user.userstatus == "Patient":
        #patient = Patient.query.get(current_user.id)
        #therapist = Therapist.query.get()
        #request.acceptRequest(therapist.id, patient.id)
        request.status = "accepted"
        accepted_request = T_Patients(id = request.id, t_id = request.origin , p_id = current_user.id, response = "accepted")
        therapist = Therapist.query.get(request.origin)
        therapist.numPatients += 1
        patient = Patient.query.get(current_user.id)
        patient.hasTherapist = True
        patient.T_ID = therapist.therapistName
        db.session.add(accepted_request)
        db.session.commit()

    request.status = "accepted"
    flash('you have accepted the request')

    return render_template('accountview.html')

@bp.route('/decline/<int:id>/<int:origin>')
@login_required
def decline(id,origin):

    request = Request.query.get(id)
    origin = Request.query.get(origin)

    id = current_user.id
    user = current_user

    if current_user.userstatus == "Therapist":
        declined_request = T_Patients(id = request.id, t_id = current_user.id, p_id = request.origin, response = "declined")
        db.session.add(accepted_request)
        db.session.commit()


    if current_user.userstatus == "Patient":
        declined_request = T_Patients(id = request.origin, p_id = current_user.id, response = "declined")
        db.session.add(accepted_request)
        db.session.commit()
    
    #therapist.numPatients += therapist.numPatients
    patient.hasTherapist = False

    return render_template('accountview.html')



@bp.route('/removetherapist/<int:id>')
@login_required
def removetherapist(id):

    mytherapist = T_Patients.query.filter_by(t_id = id).one()
    therapist = Therapist.query.get(id = id)
    therapist.numPatients -=1 
    patient = Patient.query.get(id = current_user.id)
    patient.T_ID = None
    patient.hasTherapist = False
    db.session.delete(mytherapist)
    db.session.commit()

    flash('you have deleted your therapist')

    return render_template('accountview.html') 

@bp.route('/removepatient/<int:id>')
@login_required
def removepatient(id):

    #patients = Patient.query.filter_by()
    #mypatientT_Patients.query.filter_by(p_id = id)
    #patients = Patients.query.filter_by(T_ID = current_user.id)
    mypatient = T_Patients.query.filter_by(p_id = id).one()
    therapist = Therapist.query.get(id = current_user.id)
    therapist.numPatients -=1 
    patient = Patient.query.get(id = id )
    patient.hasTherapist = False
    db.session.delete(mypatient)
    db.session.commit()

    flash('you have deleted your patient')

    return render_template('accountview.html') 

@bp.route('/affirmation', methods = ['GET', 'POST'])
@login_required
def affirmation():
    form = createAEntry()

    if form.validate_on_submit():
        a = models.AffirmationEntry(AffirmationEntryTitle=form.EntryTitle.data, AffirmationEntryText=form.EntryText.data)
        db.session.add(a)
        db.session.commit()
        flash('Affirmation has been created!', category='success')
        return redirect(url_for('main.index'))
    return render_template('affirmation.html', AffirmationEntry=AffirmationEntry, form=form)


@bp.route('/viewAffirmation')
def affirmationview():
    affirmationEntries=AffirmationEntry.query.all()
    return render_template('affirmationview.html', entries=affirmationEntries)

@bp.route('/deleteAffirmation/<int:AffirmationEntryID>', methods=['POST', 'GET', 'DELETE'])
def deleteAffirmation(AffirmationEntryID):

    entry = AffirmationEntry.query.filter_by(AffirmationEntryID = AffirmationEntryID).first()

    db.session.delete(entry)
    db.session.commit()
    entries = AffirmationEntry.query.all()

    return render_template('affirmationview.html', entries=entries)
    entry = JournalEntry.query.get(EntryID)

#chatbot files
bot = ChatBot("Chatbot Therapist")
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
    "What is your name?",
    "My name is Bot Therapist.",
    "Who are you?",
    "I am your private mental health therapist."
]
trainer = ListTrainer(bot)
trainer.train(conversation)
#training on english dataset
#for files in os.listdir('./english/'):
#    data=open('./english/'+files,'r').readlines()
#    bot.train(data)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')



@bp.route("/chat")
def chat():
    return render_template("chat.html")

@bp.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = HelpDeskForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.Subject.data, sender='sentijournalapp@gmail.com', recipients=['incoming+sentijournal-supportticketing-15617391-issue-@incoming.gitlab.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.Name.data, form.Email.data, form.Message.data)
            mail.send(msg)
            flash('Thank you for your message! We will get back to you shortly', category='success')
            return redirect(url_for('main.contact'))
            return render_template('contact.html', success=True, form=form)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)
        
@bp.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))
