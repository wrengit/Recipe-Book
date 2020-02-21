
from werkzeug.security import check_password_hash
from app import login, mongo


# https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb
# https://github.com/boh717/FlaskLogin-and-pymongo

# add a user class for Flask-login. Flask-login requires four attribute to be defined
# These are defined below.
class User():
    def __init__(self, username, email, _id, is_admin):
        self.username = username
        self.email = email
        self._id = _id
        self.is_admin = is_admin
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
        
    # Uses 'check_password_hash' from werkzeug.security to compare hashed PW stored in DB
    # against users entered password.
    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

# Flask-login uses the 'user_login' to manage the users session. Requires a unique id for each
# user. In these modesl the username is the unique ID for each user. User model stores user 
# attributes from the DB (email, id, is_admin)
@login.user_loader
def load_user(username):
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return None
    return User(user['username'], user['email'], user['_id'], user['is_admin'])
