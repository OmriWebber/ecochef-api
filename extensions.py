from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()