from flask import render_template, redirect, flash, url_for, request
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import app, mongo
from app.forms import UserLoginForm, UserRegistrationForm, RecipeForm
from app.users import User
from bson import ObjectId


@app.route('/')
@app.route('/index')
def index():
    recipes = mongo.db.recipes.find({})
    return render_template('index.html', recipes=recipes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data})
        if user and User.check_password(user['password'], form.password.data):
            user_obj = User(user['username'], user['email'], user['_id'], user['is_admin'])
            login_user(user_obj)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
    return render_template('loginform.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        pwhash = generate_password_hash(form.password.data)
        mongo.db.users.insert_one({
            'username': form.username.data,
            'email': form.email.data,
            'password': pwhash,
            'is_admin': False
        })
        flash('You are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/postrecipe', methods=['GET', 'POST'])
@login_required
def postrecipe():
    form = RecipeForm()
    if form.validate_on_submit():
        mongo.db.recipes.insert_one({
            'name': form.recipe_name.data,
            'desc': form.recipe_desc.data,
            'ingredients': form.ingredients.data,
            'method': form.method.data,
            'owner': current_user.username,
            'tags': form.tags.data
        })
        flash('Recipe added!')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', form=form, title='Post Recipe')

#deletes a recipe. Initially this was tried with an ajax (DELETE) call
# but this threw HTTP 500 errors. 
#QUESTION? what's the negatives in using a GET req. for this purpose?
@app.route('/deleterecipe/<id>')
@login_required
def delete(id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    if current_user.username == recipe['owner'] or current_user.is_admin:
        mongo.db.recipes.delete_one({"_id": ObjectId(id)})
        flash('Recipe Deleted')
        return redirect(url_for('index'))
    flash('Action not allowed')
    return redirect(url_for('index'))


@app.route('/editrecipe/<id>', methods=['GET', 'POST'])
@login_required
def editrecipe(id):
    form = RecipeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            mongo.db.recipes.update_one({"_id": ObjectId(id)}, {"$set": {
                'name': form.recipe_name.data,
                'desc': form.recipe_desc.data,
                'ingredients': form.ingredients.data,
                'method': form.method.data,
                'owner': current_user.username,
                'tags': form.tags.data
            }})
            flash('Recipe Updated')
            return redirect(url_for('index'))
        return render_template('add_recipe.html', form=form, title='Edit Recipe')

    elif request.method == "GET":
        recipe = mongo.db.recipes.find_one(
            {"_id": ObjectId(id)})
        form.recipe_name.data = recipe['name']
        form.recipe_desc.data = recipe['desc']
        for ingredient in recipe['ingredients']:
            form.ingredients.append_entry(data=ingredient)
        form.method.data = recipe['method']
        form.tags.data = ', '.join(map(str, recipe['tags']))
        return render_template('add_recipe.html', form=form, title='Edit Recipe')
