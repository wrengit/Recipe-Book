from flask import render_template, redirect, flash, url_for, request, json
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import app, mongo
from app.forms import UserLoginForm, UserRegistrationForm, RecipeForm, SearchForm
from app.users import User
from bson import ObjectId

# Index. Populates index with all recipes in db.
# All routes require 'search_form', as this is located in the navbar
# which renders on each page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    recipes = mongo.db.recipes.find({})
    if request.method == 'POST':
        return redirect(url_for('search_results', ingredient=search_form.search.data))
    return render_template('index.html', recipes=recipes, search_form=search_form, title='Recipe Book')

# Login route. If user is logged in then redirects to the index page. Uses the 'User'
# model from 'users.py' to login with flask-login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserLoginForm()
    search_form = SearchForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data})
        if user and User.check_password(user['password'], form.password.data):
            user_obj = User(user['username'], user['email'],
                            user['_id'], user['is_admin'])
            login_user(user_obj)
            # accesses the 'next page' query string to determine which url user wanted to visit
            # before being redirected to the login page. If no next page was given then redirects user
            # to the index page. 'url_parse.netloc' prevents malicious redirect attacks. This prevents
            #redirects by ensuring that the url is relative to the page. 
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Wrong username or password', 'warning')
    return render_template('loginform.html', form=form, search_form=search_form, title='Login')

# Logout route. Logs user out of the session managemnt provided by Flask-login and redirects
# logged out use to the index page. @login_required is a func from Flask-login which prevents
# users accessing specific locations. Redirects users to the login page.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register new user.
# Writes a new user to the 'users' collection in the DB. This sets the user 'is_admin' boolean
# to false for each new user. The only way to change this value is directly in the DB.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    search_form = SearchForm()
    if form.validate_on_submit():
        pwhash = generate_password_hash(form.password.data)
        mongo.db.users.insert_one({
            'username': form.username.data,
            'email': form.email.data,
            'password': pwhash,
            'is_admin': False
        })
        flash('You are now registered', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, search_form=search_form, title='Register')

# Profile route, displays recipes on profile page owned by user.
# 'recipes' shows all recipes which the user owns, and 'like_recipes' shows all recipes
# that the user has liked.
@app.route('/profile/<username>')
def profile(username):
    search_form = SearchForm()
    recipes = mongo.db.recipes.find({"owner": current_user.username})
    liked_recipes = mongo.db.recipes.find({"likes": current_user.username})
    return render_template('profile.html', recipes=recipes, search_form=search_form, liked_recipes=liked_recipes, title='Profile')

# Post recipe
# posts a new recipes to the 'recipes' DB col.
@app.route('/postrecipe', methods=['GET', 'POST'])
@login_required
def postrecipe():
    form = RecipeForm()
    search_form = SearchForm()
    if form.validate_on_submit():
        mongo.db.recipes.insert_one({
            'name': form.recipe_name.data,
            'desc': form.recipe_desc.data,
            'ingredients': form.ingredients.data,
            'method': form.method.data,
            'owner': current_user.username,
            'tags': form.tags.data,
            'image': form.image.data,
            'likes': []
        })
        flash('Recipe added!', 'success')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', form=form, search_form=search_form, title='Post Recipe')

# Delete a recipe
# uses the recipes 'id' to delete a recipe from the recipes col. Users must be logged in to view this route
# Users may only delete a recipe if their username matches the owner field on the recipe.
@app.route('/deleterecipe/<id>')
@login_required
def delete(id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    # Only allows recipe owner or admin to delete recipe
    if current_user.username == recipe['owner'] or current_user.is_admin:
        mongo.db.recipes.delete_one({"_id": ObjectId(id)})
        flash('Recipe Deleted', 'success')
        return redirect(url_for('index'))
    flash('Action not allowed', 'warning')
    return redirect(url_for('index'))

# Edit recipe
# Allows user to edit their recipe. Ensure only logged in users can access and that their username
# matches the owner field in recipe. This view preopulates the form with the current recipes info.
@app.route('/editrecipe/<id>', methods=['GET', 'POST'])
@login_required
def editrecipe(id):
    form = RecipeForm()
    search_form = SearchForm()
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    # stops user editing recipes not owned by finding recipe id in source code
    if current_user.username == recipe['owner'] or current_user.is_admin:
        if request.method == "POST":
            if form.validate_on_submit():
                mongo.db.recipes.update_one({"_id": ObjectId(id)}, {"$set": {
                    'name': form.recipe_name.data,
                    'desc': form.recipe_desc.data,
                    'ingredients': form.ingredients.data,
                    'method': form.method.data,
                    'tags': form.tags.data,
                    'image': form.image.data,
                    'owner': current_user.username
                }})
                flash('Recipe Updated', 'info')
                return redirect(url_for('index'))
            return render_template('add_recipe.html', form=form, search_form=search_form, title='Edit Recipe')
        elif request.method == "GET":
            # Populates recipe form with data from db
            form.recipe_name.data = recipe['name']
            form.recipe_desc.data = recipe['desc']
            for ingredient in recipe['ingredients']:
                form.ingredients.append_entry(data=ingredient)
            form.method.data = recipe['method']
            form.image.data = recipe['image']
            form.tags.data = ', '.join(map(str, recipe['tags']))
            return render_template('add_recipe.html', form=form, search_form=search_form, title='Edit Recipe')
        flash('Action not allowed', 'warning')
        return redirect(url_for('index'))


# Search for ingredients
# Performs a full text search of the ingredietns index on the recipes col. If a text match is found
# return the results as 'recipes'. If not match is found, directs user to 'non_found.html' which
# tells user that no matches were found.
@app.route('/search_results/<ingredient>', methods=['GET', 'POST'])
def search_results(ingredient):
    search_form = SearchForm()
    recipes = list(mongo.db.recipes.find({'$text': {'$search': ingredient}}))
    if request.method == 'GET':
        if recipes:
            return render_template('search_results.html', title='Search Results', recipes=recipes, ingredient=ingredient, search_form=search_form)
        return render_template('none_found.html', search_form=search_form, title="No Recipes Found")
    elif request.method == 'POST':
        return redirect(url_for('search_results', ingredient=search_form.search.data))
    return redirect(url_for('index'))

#Like route
# Allows user to 'like' a recipe. This adds the users 'username' to an array on the recipe in recipes col.
# Route checks that the users username is in the array. If already in the array, this route wil remove the 
# users username from the array. This ensures that users cannot 'like' a recipe multiple times, artifically
# increasing the like count. This route is access through an AJAZ call in JS, and returns a json reply,
# instead of a url redirect. This ensures the page does no reload, navigating the user away from the recipe
# card.
@app.route('/like/<id>', methods=['GET', 'POST'])
def like(id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    if current_user.is_authenticated:
        if request.method == 'GET':
            like_count = len(recipe['likes'])
            return json.dumps({like_count})
        if current_user.username not in recipe['likes']:
            mongo.db.recipes.update_one({"_id": ObjectId(id)},
                                        {'$push': {'likes': current_user.username}})
            return json.dumps({'status': 'success'})
        elif current_user.username in recipe['likes']:
            mongo.db.recipes.update_one({"_id": ObjectId(id)},
                                        {'$pull': {'likes': current_user.username}})
            return json.dumps({'status': 'success'})
        flash('Action not allowed', 'warning')
        return redirect(url_for('index'))
