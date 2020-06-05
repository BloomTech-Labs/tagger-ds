import os
from dotenv import load_dotenv

load_dotenv('.env')


class Config:
    """ Base configuration """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    DEBUG = os.environ.get('DEBUG')
