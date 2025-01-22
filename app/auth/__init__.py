from flask import Blueprint

# Used to definite the login and registration parts
bp = Blueprint("auth", __name__)

from app.auth import routes