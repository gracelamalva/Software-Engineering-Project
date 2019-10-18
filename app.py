from app import create_app
from flask import Flask
from app.main_project.app.models import db

def main():
    if (len(sys.argv) == 2):
        print(sys.argv)
    if sys.argv[1] == 'createdb':
        db.create_all()
    else:
        print("Run app using 'flask run'")
        print("To create a database use 'python app.py createdb")

app = create_app