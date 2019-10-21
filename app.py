from app import create_app
import sys, csv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app.main.config import Config
from app.main.models import *

app = Flask(__name__)
app = create_app()

def populate():
    f = open("user.csv")
    reader = csv.reader(f)

    for Username, fullName, Email, passwordHash in reader: 
        db.execute("INSERT INTO User (Username, fullName, Email, passwordHash) VALUES (:Username, :fullName, :Email, :passwordHash)",
        {"Username" : Username, "fullName": fullName, "Email": Email, "passwordHash": passwordHash})
    db.commit()

def main():
    if (len(sys.argv) == 2):
        print(sys.argv)
    if sys.argv[1] == 'createdb':
        db.create_all()
    if sys.argv[1] == 'populate':
        populate()

    else:
        print("Run app using 'flask run'")
        print("To create a database use 'python app.py createdb")

if __name__ == "__main__":
    with app.app_context():
        main()
#app.config.from_object(Config)
