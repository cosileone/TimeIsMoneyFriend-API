from flask import render_template
from . import site


@site.route('/')
def homepage():
    return render_template('index.html')

@site.route('/recipes')
def recipes():
    return render_template('recipe_search.html')
