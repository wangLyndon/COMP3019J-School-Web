from flask import Blueprint

# Used to definite the main parts

bp = Blueprint('main', __name__)

from app.main import routes