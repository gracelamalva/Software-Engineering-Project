from app import app
from app import database
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import Config
from models import *



if __name__ == "__main__":
    app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': database.dbConnection()}