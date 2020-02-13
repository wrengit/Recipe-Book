
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
app.config['MONGO_URI'] = Config.MONGO_URI
mongo = PyMongo(app)


from app import views, users, errors