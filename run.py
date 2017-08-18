from flask import Flask
from flask_mysqldb import MySQL

from timf.api import api
from timf.website import site

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')
mysql = MySQL(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(site)

if __name__ == "__main__":
    app.run()
