
from flask import Flask
from config import Config, MONGO_URI
from flask_login import LoginManager
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
app.config['MONGO_URI'] = "mongodb+srv://root:AshaJuno@cluster0-fxdbe.mongodb.net/cookbook?retryWrites=true&w=majority"
mongo = PyMongo(app)


from app import views, users