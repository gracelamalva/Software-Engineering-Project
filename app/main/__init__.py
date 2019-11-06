from flask import Blueprint
#-------------
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login = LoginManager()
flask_bcrypt = Bcrypt()

bp = Blueprint('main', __name__, template_folder='templates')

from . import routes
from . import models
#-----------------------------

#bp = Blueprint('main',__name__, template_folder= '../main/templates')

#from app.main import routes
from app.main import config
#from app.main import models
