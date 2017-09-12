from flask import Flask
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='timf/website/static', instance_path=BASE_DIR+'/instance/', instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
mysql = MySQL(app)
sql_alchemy = SQLAlchemy(app)

from timf.api import api
from timf.website import site

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(site)

if __name__ == "__main__":
    app.run()
