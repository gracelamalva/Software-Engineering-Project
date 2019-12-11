from flask import Blueprint, Flask
#-------------
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


from app import api
from flask import Blueprint
from flask_mail import Mail, Message
bp = Blueprint('main',__name__, template_folder= '../main/templates')

db = SQLAlchemy()
login = LoginManager()
flask_bcrypt = Bcrypt()
mail = Mail()


bp = Blueprint('main', __name__, template_folder='templates')

from . import routes
from . import models
#-----------------------------

#bp = Blueprint('main',__name__, template_folder= '../main/templates')

#from app.main import routes
from app.main import config
#from app.main import models

def create_app():
    app = Flask(__name__)
    
    # db.init_app(app)

    app.config.from_object(config)
    
    db.init_app(app)


    #
    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    from app.api import mod
    app.register_blueprint(api.routes.mod)
    return app
