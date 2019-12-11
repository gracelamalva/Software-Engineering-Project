from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from app.main.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main import db, flask_bcrypt, login
    from app.main import models
    db.init_app(app)
    mail=Mail()
    mail.init_app(app)
    flask_bcrypt.init_app(app)
    login.init_app(app)
    login.login_view = 'main.login'

    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    
    return app
