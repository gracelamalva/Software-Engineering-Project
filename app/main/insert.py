from flask_sqlalchemy import *
import os, sys, csv
from config import Config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models import *

db = SQLAlchemy()

def populate():
   # f = open("/user.csv")
   # reader = csv.reader(f)
    
    sql = "INSERT INTO User (Username, fullName, Email, passwordHash) VALUES (%s, %s)"
    val = ("glamalva", "grace lamalva", "glamalva@gmail.com", "f3sds")
    db.session.execute(sql, val)

    db.commit()

    print(db.rowcount, "record inserted.")


  #  for Username, fullName, Email, passwordHash in reader: 
   #     db.execute("INSERT INTO User (Username, fullName, Email, passwordHash) VALUES (:Username, :fullName, :Email, :passwordHash)",
    #    {"Username" : Username, "fullName": fullName, "Email": Email, "passwordHash": passwordHash})
   # db.commit()

populate()