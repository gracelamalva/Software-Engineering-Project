from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from app.main import models

def create_app():

    app = Flask(__name__)
    #db.init_app(app)

    #
    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    from app.api import mod
    app.register_blueprint(api.routes.mod)
    return app

    
