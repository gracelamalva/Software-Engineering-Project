from flask import Blueprint
bp = Blueprint('main',__name__, template_folder= '../main/templates')

from app.main import routes
from app.main import config
from app.main import models