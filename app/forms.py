from app import mongo
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from flask_wtf import FlaskForm
from wtforms import(
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectMultipleField,
    FieldList, 
    widgets
)


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Enter your Username')])
    password = PasswordField('Password', validators=[DataRequired('Enter your Password')])
    login = SubmitField('Login')


class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please choose a Username')])
    email = StringField('Email', validators=[DataRequired('Enter your email address'), Email()])
    password = PasswordField('Password', validators=[DataRequired('Choose a Password')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired('Please re-type your Password'), EqualTo('password')])
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
    recipe_name = StringField('Recipe name', validators=[DataRequired('Enter a recipe name')])
    recipe_desc = StringField('Description', validators=[DataRequired('Give a short recipe description')])
    ingredients = FieldList(StringField('', validators=[DataRequired('Enter ingredient')]), render_kw={'class':'list-group list-group-flush'}, validators=[DataRequired('Enter at least one ingredient')])
    method = TextAreaField('Method', validators=[DataRequired('Detail the recipe method')])
    tags = SelectMultipleField(choices=[('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('healthy', 'Healthy'), ('guilty', 'Guilty Pleasure'), ('snack', 'Snack'), ('main', 'Main'), ('dessert', 'Dessert')], option_widget = widgets.CheckboxInput())
    submit = SubmitField('Submit')
