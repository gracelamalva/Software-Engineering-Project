import os

basedir = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = True
    
    
    DEBUG=True
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME = 'sentijournalapp@gmail.com'
    MAIL_PASSWORD = 'sentijournalapp'





