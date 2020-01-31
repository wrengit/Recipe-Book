from flask import render_template
from app import app
from app.forms import UserLoginForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('loginform.html', form=form)