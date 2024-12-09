from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

class User(mongo.Document):
    username = mongo.StringField(required=True, unique=True)
    password = mongo.StringField(required=True)
    role = mongo.StringField(required=True)  # e.g., Admin, Department Head, User
    department = mongo.StringField(required=True)  # e.g., Research, CSE