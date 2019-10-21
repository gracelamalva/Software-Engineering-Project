import sys
from app.main import bp
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify
from app.main.models import *
from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#bp = Blueprint("site", __name__)


#db.init_app(app)

@bp.route('/', methods=['GET','POST'])
def index():
   
    return render_template('index.html')

@bp.route('/journal', methods = ['GET', 'POST'])    
def journal():
    #entry = request.form.get("entry")
    entries = JournalEntry.query.all()
    return render_template('journal.html', entries = entries)

@bp.route('/createjournal', methods = ['POST', 'GET'])
def createjournal():

    title = request.form.get("title")
    journal = Journal(title = title)
    Users.add_journal(journal, title = title)

    db.session.add(journal)
    db.session.commit()
    # Query database.

    journal=Journal.query.all()
    return render_template('createjournal.html',journal = journal)


@bp.route('/edit', methods = ['GET', 'POST'])
def edit():
    entry = ['entry']

    if request == 'POST':
        result = request.form.get("entry")
        #update db
    
    return render_template('edit.html', entry = entry)

@bp.route('/add/', methods = ['GET', 'POST'])
def add():

    journal = Journal.query.get(JournalID)
    
    if request.method == 'POST':
       
        entrytitle = request.form.get("entrytitle")
        entrytext = request.form.get("entrytext")
        datetime = request.form.get("datetime")
        journal.add_entry(entrytitle,entrytext,datetime)
        # Equivalent to:
        # INSERT INTO flights (flight_number, origin, destination, durations) VALUES (origin,...)
        entry = journal.entries

        db.session.add(entry)
        db.session.commit()
        # Query database.

        return render_template('view.html', journal = journal, entry = entry)
    return render_template('add.html', journal = journal, entry = entry)

@bp.route('/view/<int:JournalID>', methods = ['POST','GET'])
def view(JournalID):
    journal = Journal.query.get(JournalID)
    entries = JournalEntry.query.all(journal)

    return render_template('view.html', entries = entries)

@bp.route('/delete', methods = ['POST', 'GET'])
def delete():

    return render_template('delete.html')
"""
@bp.route('/analyze', methods = ['GET', 'POST'])
def analyze():
    #template for the analyzed text -- the results from watson api

    return render_template('analyze.html')

@app.route("/<string:username>/journal")
def journal():
    #username = username
    return render_template('journal.html', username = username)
"""