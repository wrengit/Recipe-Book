
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login, mongo


# https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb
# https://github.com/boh717/FlaskLogin-and-pymongo

class User():
    def __init__(self, username, email, _id):
        self.username = username
        self.email = email
        self._id = _id

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
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return None
    return User(user['username'], user['email'], user['_id'])
