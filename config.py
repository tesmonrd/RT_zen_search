import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']