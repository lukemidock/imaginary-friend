from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    DEBUG = False
    TESTING = False
    SQL_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI")
    DEFAULT_MODE = 'config.DevelopmentConfig'

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get("PRODUCTION_SECRET")

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = environ.get("DEVELOPMENT_SECRET")