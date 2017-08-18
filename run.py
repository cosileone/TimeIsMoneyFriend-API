from flask import Flask
from flask_mysqldb import MySQL

from timf.api.views import items
from timf.website import home

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')
mysql = MySQL(app)

app.register_blueprint(items, url_prefix='/api')
app.register_blueprint(home)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    app.run()
