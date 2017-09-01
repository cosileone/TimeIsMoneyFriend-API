from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='timf/website/static')
app.config.from_object('config')
app.config.from_pyfile('config.py')
mysql = MySQL(app)

from timf.api import api
from timf.website import site

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(site)

if __name__ == "__main__":
    app.run()
