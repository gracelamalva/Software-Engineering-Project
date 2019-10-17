from flask import Flask, current_app

def create_app():

    app = Flask(__name__)

    #
    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    from app.api import mod
    app.register_blueprint(api.routes.mod)
    return app

    
