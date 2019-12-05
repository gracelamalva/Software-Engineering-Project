from flask import Flask

from app.main.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.main import db, flask_bcrypt, login, mail
    db.init_app(app)
    flask_bcrypt.init_app(app)
    login.init_app(app)
    login.login_view = 'main.login'
    mail.init_app(app)

    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app
