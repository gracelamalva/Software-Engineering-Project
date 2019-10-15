from app.main import bp
from flask import Flask, render_template, request, Blueprint

#from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#bp = Blueprint("site", __name__)

@bp.route('/', methods=['GET','POST'])
def index():
    #return "This is a basic route."
    return render_template('index.html')

@bp.route('/journal', methods = ['GET', 'POST'])    
def journal():
    #entry = request.form.get("entry")
    return render_template('journal.html')
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