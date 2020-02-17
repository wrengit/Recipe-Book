from flask import render_template, redirect, flash, url_for, request, json
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import app, mongo
from app.forms import UserLoginForm, UserRegistrationForm, RecipeForm, SearchForm
from app.users import User
from bson import ObjectId

# Index. Populates index with all recipes in db
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    recipes = mongo.db.recipes.find({})
    if request.method == 'POST':
        return redirect(url_for('search_results', ingredient=search_form.search.data))
    return render_template('index.html', recipes=recipes, search_form=search_form)

# Login
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
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Wrong username or password', 'warning')
    return render_template('loginform.html', form=form, search_form=search_form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register new user
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
    return render_template('register.html', form=form, search_form=search_form)

# Profile route, displays recipes on profile page owned by user
@app.route('/profile/<username>')
def profile(username):
    search_form = SearchForm()
    recipes = mongo.db.recipes.find({"owner": current_user.username})
    liked_recipes = mongo.db.recipes.find({"likes": current_user.username})
    return render_template('profile.html', recipes=recipes, search_form=search_form, liked_recipes=liked_recipes)

# Post recipe
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
@app.route('/deleterecipe/<id>')
@login_required
def delete(id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    # Only allows recipe owner or admin to delete recipe
    if current_user.username == recipe['owner'] or current_user.is_admin:
        mongo.db.recipes.delete_one({"_id": ObjectId(id)})
        flash('Recipe Deleted', 'success')
        return redirect(url_for('index'))
    flash('Action not allowed')
    return redirect(url_for('index'))

# Edit recipe
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
@app.route('/search_results/<ingredient>', methods=['GET', 'POST'])
def search_results(ingredient):
    search_form = SearchForm()
    recipes = list(mongo.db.recipes.find({'$text': {'$search': ingredient}}))
    if request.method == 'GET':
        if recipes:
            return render_template('search_results.html', recipes=recipes, ingredient=ingredient, search_form=search_form)
        return render_template('none_found.html', search_form=search_form)
    elif request.method == 'POST':
        return redirect(url_for('search_results', ingredient=search_form.search.data))
    return render_template('index.html', recipes=recipes, search_form=search_form)


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
