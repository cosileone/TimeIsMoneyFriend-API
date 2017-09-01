from flask import render_template
from . import site
from run import mysql


@site.route('/')
def homepage():
    return render_template('base.html')
