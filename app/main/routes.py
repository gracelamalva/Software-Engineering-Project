import sys, csv, os, datetime
from datetime import timedelta
from sqlalchemy.testing import db
from werkzeug.urls import url_parse
from app.main import bp, models
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify, flash
from app.main import bp, models
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify
from app.main.models import *
from .models import Users
from .models import Journal
from .models import JournalEntry
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from app.main.config import Config
# from app.api.request import *
from app.api.request import analyze

from flask_login import login_required, current_user, logout_user, login_user
from .forms import RegisterForm, LoginForm, ChangePasswordForm, UpdateAccountInfo, createAEntry


@bp.route('/', methods=['GET','POST'])
def index():
    user = current_user

    return render_template('index.html', user = user)

#------------ user login routes ----------

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
    return render_template('accountview.html')

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

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

#------------ user login routes ----------


@bp.route('/journal', methods = ['GET', 'POST'])
def journal():
    # entry = request.form.get("entry")
    entries = JournalEntry.query.all()
    return render_template('journal.html', journal = journal, entries=entries)


@bp.route('/search', methods=['GET', 'POST'])
def search():#JournalID):
    dt = request.args.get("date")
    ft = '%Y-%m-%d'
    date = datetime.strptime(dt, ft)
    entries = JournalEntry.query.filter(JournalEntry.Date_Time.between(date, date + datetime.timedelta(days=1))).all()
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
    # entries = JournalEntry.query.all()

    if request.method == "POST":
        # journal =Journal.query.get(JournalID)
        entrytitle = request.form.get("title")
        entrytext = request.form.get("entry")
        dt = request.form.get("date-time")
        ft = '%Y-%m-%dT%H:%M'
        result = datetime.strptime(dt, ft)

        journal.add_entry(entrytitle, entrytext, result)
       
        #entries = journal.entries
        #entry = JournalEntry(EntryTitle = entrytitle, EntryText = entrytext, Date_Time = datetime)
        #entry = journal.add_entry(entrytitle, entrytext, result)
        #db.session.add(entry)
        #db.session.commit()
    entries = JournalEntry.query.all()
    return render_template('journal.html', journal=journal, entries=entries)


@bp.route('/delete/<int:EntryID>', methods=['POST', 'GET', 'DELETE'])
def delete(EntryID):
    #entry = JournalEntry.query.get(EntryID)

    #JournalEntry.query.filter_by(EntryID = EntryID).delete()
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

    therapists = Therapist.query.all()

    return render_template('findtherapist.html', therapists = therapists )

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
