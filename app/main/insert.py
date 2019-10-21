from flask_sqlalchemy import *
import os, sys, csv

db = SQLAlchemy()

def populate():
    f = open("user.csv")
    reader = csv.reader(f)

    for Username, fullName, Email, passwordHash in reader: 
        db.execute("INSERT INTO User (Username, fullName, Email, passwordHash) VALUES (:Username, :fullName, :Email, :passwordHash)",
        {"Username" : Username, "fullName": fullName, "Email": Email, "passwordHash": passwordHash})
    db.commit()

populate()