# Based on code from Faraz, Vulnerable App

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # This key is supposed to prevent CSRF attacks which you are not being tested
    # on for this lab. Please ignore it
    SECRET_KEY = "this-is-a-secret-key"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@172.16.0.2:3306/demodb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
