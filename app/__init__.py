import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

# Configuring Logging
logger = logging.getLogger()

# Lower the log level to make it can custom input log information
logger.setLevel(logging.INFO)
# Set the format of the log
logFormat = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
# Ignore werkzeug information
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# Set the login level log
loginHandler = RotatingFileHandler("./app/log/login.log", maxBytes=5242880, backupCount=2)
loginHandler.setLevel(logging.INFO)
loginHandler.setFormatter(logFormat)
loginHandler.addFilter(lambda logName: logName.name == "login")
logger.addHandler(loginHandler)

# Set the register level log
registerHandler = RotatingFileHandler("./app/log/register.log", maxBytes=5242880, backupCount=2)
registerHandler.setLevel(logging.INFO)
registerHandler.setFormatter(logFormat)
registerHandler.addFilter(lambda logName: logName.name == "register")
logger.addHandler(registerHandler)

# Set the announcement level log
announcementHandler = RotatingFileHandler("./app/log/announcement.log", maxBytes=5242880, backupCount=2)
announcementHandler.setLevel(logging.INFO)
announcementHandler.setFormatter(logFormat)
announcementHandler.addFilter(lambda logName: logName.name == "announcement")
logger.addHandler(announcementHandler)

# Set the module level log
moduleHandler = RotatingFileHandler("./app/log/module.log", maxBytes=5242880, backupCount=2)
moduleHandler.setLevel(logging.INFO)
moduleHandler.setFormatter(logFormat)
moduleHandler.addFilter(lambda logName: logName.name == "module")
logger.addHandler(moduleHandler)

# Set the menu level log
menuHandler = RotatingFileHandler("./app/log/menu.log", maxBytes=5242880, backupCount=2)
menuHandler.setLevel(logging.INFO)
menuHandler.setFormatter(logFormat)
menuHandler.addFilter(lambda logName: logName.name == "menu")
logger.addHandler(menuHandler)

# Set the account level log
accountHandler = RotatingFileHandler("./app/log/account.log", maxBytes=5242880, backupCount=2)
accountHandler.setLevel(logging.INFO)
accountHandler.setFormatter(logFormat)
accountHandler.addFilter(lambda logName: logName.name == "account")
logger.addHandler(accountHandler)

# Set the ERROR level log
errorHandler = RotatingFileHandler("./app/log/error.log", maxBytes=5242880, backupCount=2)
errorHandler.setLevel(logging.ERROR)
errorHandler.setFormatter(logFormat)
errorHandler.addFilter(lambda logType: logType.levelno == logging.ERROR)
logger.addHandler(errorHandler)

# Users who are not logged in will be returned here when access an interface that requires login
login = LoginManager(app)
login.login_view = "auth.login"
login.init_app(app)

from app.auth import bp as auth_bp

app.register_blueprint(auth_bp, url_prefix="/auth")

from app.main import bp as main_bp

app.register_blueprint(main_bp)

from app.admin import bp as admin_bp

app.register_blueprint(admin_bp, url_prefix="/admin")

with app.app_context():
    db.create_all()

from app import models
