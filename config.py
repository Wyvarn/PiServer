import os

basedir = os.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get()
    CSRF_ENABLE = True
    CSRF_SESSION_KEY = os.environ.get()
    DEBUG = False