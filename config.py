# config.py
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ecochef'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    if 'RDS_HOSTNAME' in os.environ:
        print('AWS ELB ENV DETECTED')
        RDS_Connection_String = 'mysql+pymysql://' + os.environ['RDS_USERNAME'] + ':' + os.environ['RDS_PASSWORD'] + '@' + os.environ['RDS_HOSTNAME'] + ':' + os.environ['RDS_PORT'] + '/' + os.environ['RDS_DB_NAME']
        SQLALCHEMY_DATABASE_URI = RDS_Connection_String
    else:
        print('No Database Detected, using local database')
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:password@ecochef-api.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com:3306/ecochef_api'
        # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/ecochef-api'
        