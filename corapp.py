from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#export APP_SETTINGS="config.DevelopmentConfig
app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)