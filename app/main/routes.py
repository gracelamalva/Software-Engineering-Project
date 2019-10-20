import sys
from app.main import bp
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify
from app.main.models import *
from .models import Users
from .models import Journal
from .models import JournalEntry
from flask_sqlalchemy import SQLAlchemy

from config import Config
from sqlalchemy.testing import db

app = Flask(__name__)
app.config.from_object(Config)
bp = Blueprint("site", __name__)

db.init_app(app)

@bp.route('/', methods=['GET','POST'])
def index():
   
    return render_template('index.html')

@bp.route('/journal', methods = ['GET', 'POST'])    
def journal():
    #entry = request.form.get("entry")
    entries = ['sample']

    #if request.method == 'POST':
     #   result = request.form.get("entry")
      #  entries.append(result)

       # return redirect(url_for('main.edit'))
    
   # if request.method == 'GET':
    #  return redirect(url_for('main.view'))

    return render_template('journal.html', entries=entries)

@bp.route('/createjournal', methods = ['POST', 'GET'])
def create_journal():
    title = request.form.get("title")
    username = request.form.get("username")
    journal = Journal(title=title, username=username)
    db.session.add(journal)
    db.session.commit()
    # Query database.
    journal=Journal.query.all()
    return render_template('createjournal.html', journal=journal)

@bp.route('/edit', methods = ['GET', 'POST'])
def edit(EntryID):
    entry = ['entry']

    if request == 'POST':
        result = request.form.get("entry")
        #update db
        #looks for Journal Entry (using user login and journal id) deletes old entry and replaces with new one
    
    return render_template('edit.html', entry = entry)

@bp.route('/add/<int:JournalID>', methods = ['GET', 'POST'])
def add(JournalID):

    journal = Journal.query.get(JournalID)
    
    if request.method == 'POST':
       
        entrytitle = request.form.get("entrytitle")
        entrytext = request.form.get("entrytext")
        datetime = request.form.get("datetime")
        journal.add_entry(entrytitle, entrytext, datetime)
        # Equivalent to:
        # INSERT INTO flights (flight_number, origin, destination, durations) VALUES (origin,...)
        entry = journal.entries

        db.session.add(entry)
        db.session.commit()
        # Query database.
        entry = JournalEntry.query.all()


        return render_template('view.html', journal=journal, entry=entry)
    return render_template('add.html', journal=journal, entry=entry)

@bp.route('/view/<int:JournalID>', methods = ['POST','GET'])
def view():
    entries = JournalEntry.query.all()
    return render_template('view.html', entries = entries)

@bp.route('/delete', methods = ['POST', 'GET'])
def delete():

    return render_template('delete.html')
"""
@app.route("/")
def index():
    #journal = Journal.query.all() #Jornal from db
    return render_template('index.html') #, journal = journal)

@app.route("/<string:username>/journal")
def journal():
    #username = username
    return render_template('journal.html', username = username)
"""