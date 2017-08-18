from flask import render_template

from . import site


@site.route('/')
def homepage():
    return render_template('base.html')
