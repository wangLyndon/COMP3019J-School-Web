from flask import Blueprint

# Used to definite the admin parts
bp = Blueprint("admin", __name__)

from app.admin import routes
