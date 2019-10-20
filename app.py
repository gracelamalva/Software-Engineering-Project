from app import create_app
import sys
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


from app.main.config import Config

from app.main.models import *


def main():
    if (len(sys.argv) == 2):
        print(sys.argv)
    if sys.argv[1] == 'createdb':
        db.create_all()
    else:
        print("Run app using 'flask run'")
        print("To create a database use 'python app.py createdb")

app = create_app

#app.config.from_object(Config)
