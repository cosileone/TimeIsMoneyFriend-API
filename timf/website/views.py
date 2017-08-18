from flask import render_template
# from flask_login import login_required

from . import site


@site.route('/')
def homepage():
    return render_template('base.html')
