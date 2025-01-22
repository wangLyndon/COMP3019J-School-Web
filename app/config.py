import os

from dotenv import load_dotenv

# load .env file's config
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "neonganegjoaneguoEUGoneognoaengoaengOUENGA"
    # You need to create a .env file in the root directory to store those
    # @ should be replaced as %40 to avoid error in uri
    USERNAME = os.environ.get("WEB_USERNAME")
    PASSWORD = os.environ.get("WEB_PASSWORD")
    HOST = os.environ.get("HOST")
    DATABASE = os.environ.get("DATABASE")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False