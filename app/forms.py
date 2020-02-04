from app import mongo
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from flask_wtf import FlaskForm
from wtforms import(
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    FormField,
    FieldList,
    IntegerField,
    TextAreaField
)


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')


class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        user = mongo.db.users.find_one({'username': username.data})
        if user is not None:
            raise ValidationError(
                'Username is taken. Please select a different Username')

    def validate_email(self, email):
        user = mongo.db.users.find_one({'email': email.data})
        if user is not None:
            raise ValidationError(
                'You have already registered! Please login!')



class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe name', validators=[DataRequired()])
    recipe_desc = StringField('Description')
    ingredients = FieldList(StringField(''), min_entries=1)
    method = TextAreaField('Method', validators=[DataRequired()])
    submit = SubmitField('Submit')
