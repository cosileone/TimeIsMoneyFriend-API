from flask import Flask
from flask_mysqldb import MySQL
from api.views import items
from website import home

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'newswire.theunderminejournal.com'
app.config['MYSQL_DB'] = 'newsstand'
mysql = MySQL(app)

app.register_blueprint(items, url_prefix='/api')
app.register_blueprint(home)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    app.run(debug=True)
