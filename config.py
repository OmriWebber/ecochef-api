# config.py
import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/ecochef-api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ecochef'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
