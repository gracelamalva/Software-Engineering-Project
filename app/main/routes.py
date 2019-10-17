from app.main import bp
from flask import Flask, redirect, render_template, request, Blueprint, url_for, jsonify

#from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#bp = Blueprint("site", __name__)

@bp.route('/', methods=['GET','POST'])
def index():
    #return "This is a basic route."

    if (request.method == 'POST'):
       return redirect(url_for('main.journal'))

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

    return render_template('journal.html', entries = entries)

@bp.route('/edit', methods = ['GET', 'POST'])
def edit():
    entry = ['entry']

    if request == 'POST':
        result = request.form.get("entry")
        #update db
    
    return render_template('edit.html', entry = entry)

@bp.route('/add', methods = ['GET', 'POST'])
def add():

    entry = ['entry']

    if request == 'POST':
        result = request.form.get("entry")
        return render_template('view.html')
        #update db
    
    return render_template('add.html', entry = entry)

@bp.route('/view', methods = ['POST','GET'])
def view():
    entries = ['sample1']
    result = request.form.get("entry")
    entries.append(result)

    if request == 'POST':
        return render_template('add.html')

    return render_template('view.html', entries = entries)

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