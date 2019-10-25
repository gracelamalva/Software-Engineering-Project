import sys, csv, os, datetime
from app.main import bp
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify
from app.main.models import *
from .models import Users
from .models import Journal
from .models import JournalEntry
from flask_sqlalchemy import SQLAlchemy
from app.main.config import Config
#from app.api.request import *
from app.api.request import analyze

#bp = Blueprint("site", __name__)
db = SQLAlchemy()

@bp.route('/', methods=['GET','POST'])
def index():
    users = Users.query.all()
    return render_template('index.html', users = users)

@bp.route('/journal', methods = ['GET', 'POST'])    
def journal():
    #entry = request.form.get("entry")
    entries = JournalEntry.query.all()
    return render_template('journal.html', entries = entries)

@bp.route('/createjournal', methods = ['POST', 'GET'])
def create_journal():

    title = request.form.get("title")
    journal = Journal(title=title, UserID = "glamalva")
    db.session.add(journal)
    db.session.commit()
    # Query database.
    journal=Journal.query.all()

    return render_template('journal.html', journal=journal)

@bp.route('/edit/<int:EntryID>', methods = ['GET', 'POST', 'PUT'])
def edit(EntryID):

    entry = JournalEntry.query.get(EntryID)
    entries = JournalEntry.query.all()
    if (request.method == "POST"):
        entry.EntryTitle = request.form.get("newtitle")
        entry.EntryText = request.form.get("newtext")

    #entries = JournalEntry.query.all()
        #looks for Journal Entry (using user login and journal id) deletes old entry and replaces with new one

        return render_template('journal.html', entries = entries)

    return render_template('edit.html' , entries = entries)
    

@bp.route('/add/<int:JournalID>', methods = ['GET', 'POST'])
def add(JournalID):
    journal =Journal.query.get(JournalID)
    #entries = JournalEntry.query.all()

    if request.method == "POST":
        #journal =Journal.query.get(JournalID)
        entrytitle = request.form.get("title")
        entrytext = request.form.get("entry")
        dt = request.form.get("datetime")
        ft = '%Y-%m-%dT%H:%M'
        result = datetime.datetime.strptime(dt, ft)
        
        journal.add_entry(entrytitle, entrytext, result)

        #entries = journal.entries
        #entry = JournalEntry(EntryTitle = entrytitle, EntryText = entrytext, Date_Time = datetime)
        #entry = journal.add_entry(entrytitle, entrytext, result)
        #db.session.add(entry)
        #db.session.commit()
  
    entries = JournalEntry.query.all()
    return render_template('journal.html', journal=journal, entries = entries)

@bp.route('/delete/<int:EntryID>', methods = ['POST','GET', 'DELETE'])
def delete(EntryID):
    entry = JournalEntry.query.get(EntryID)

    JournalEntry.query.filter_by(EntryID = EntryID).delete()
    db.session.commit()
        
    entries = JournalEntry.query.all()

    return render_template('journal.html', entries = entries)


@bp.route('/analyze', methods = ['GET', 'POST'])
def analyze_text():
    #template for the analyzed text -- the results from watson api
    analyzed_text = ""
    text = request.form['entry']

    if (request.method == "POST"):
        analyzed_text =  analyze(text)
    
    
    return render_template('analyze.html', analyzed_text = analyzed_text, text = text)

"""
@bp.route('/populate', methods= ['GET','POST'])
def populate():
    query = db.insert(Users).values(Username = "glamalva", fullName='grace', passwordHash="dfsfs34", Email = "gracegmailcom") 
   # db.session.execute( "INSERT INTO Users (Username, fullName, passwordHash, Email) VALUES ('glamalva', 'gracelamalva', 'adfa43', 'glamalvagmailcom')")
    db.session.execute(query)
    db.session.commit()

    print("record inserted.")

    return render_template (url_for('main.index'))


@bp.route('/view/<int:JournalID>', methods = ['POST','GET'])
def view(JournalID):
    journal = Journal.query.get(JournalID)
    entries = JournalEntry.query.all(journal)

    return render_template('view.html', entries = entries)
"""