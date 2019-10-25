from flask import Blueprint

mod = Blueprint('api',__name__)

from app.api import routes
