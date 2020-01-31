
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, mongo


# https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb
# https://github.com/boh717/FlaskLogin-and-pymongo

class User():
    def __init__(self, username, email):
        self.username = username
        self.email=email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

@login.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"username": username})
    if not u:
        return None
    return User(u['username'], u['email'])