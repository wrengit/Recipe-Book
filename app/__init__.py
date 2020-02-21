
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login' # Flask-login uses url_for to get url for the login page
app.config['MONGO_URI'] = Config.MONGO_URI #Gets MONGO_URI string from config object
mongo = PyMongo(app) # Initializes Pymongo


from app import views, users, errors