from flask import render_template
from app import app, mongo
from app.forms import SearchForm

# Error route for HTTP 404 errors
@app.errorhandler(404)
def not_found(error):
    search_form = SearchForm()
    return render_template('/errors/404.html', search_form=search_form, title="Error"), 404

# Error route for HTTP 500 errors
@app.errorhandler(500)
def server_error(error):
    search_form=SearchForm()
    return render_template('/errors/500.html', search_form=search_form, title="Error"), 500
