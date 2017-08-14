from flask import Flask, jsonify, request
# from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'newswire.theunderminejournal.com'
# app.config['MYSQL_DB'] = 'newsstand'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@newswire.theunderminejournal.com/newsstand"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mysql = SQLAlchemy(app)

mysql.Model.metadata.reflect(mysql.engine)


class Item(mysql.Model):
    __table__ = mysql.Model.metadata.tables['tblDBCItem']

    # def __repr__(self):
    #     return "<{} - {}>".format(self.id, self.name_enus)


@app.route('/items', methods=['GET'])
def items():
    # sql = '''SELECT id, name_enus from tblDBCItem where auctionable = true;'''
    # cursor = mysql.connection.cursor()
    # cursor.execute(sql)
    # data = cursor.fetchall()
    data = Item.query.all()
    results = []
    for row in data:
        item = {}
        for tup in zip([str(column) for column in Item.metadata.tables['tblDBCItem'].columns.keys()], row[column]):
            item[tup[0]] = tup[1]

        results.append(item)

    return jsonify({"items": results})


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    sql = '''SELECT id, name_enus FROM tblDBCItem WHERE id = {} AND auctionable = true;'''.format(item_id)
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()

    if data:
        results = []
        item = {}
        for tup in zip([column[0] for column in cursor.description], data):
            item[tup[0]] = tup[1]

            results.append(item)
    else:
        return jsonify({"error": "item not found"}), 404

    return jsonify(results)


@app.route('/item/', methods=['GET'])
def resolve_item_name():
    item_name = request.args.get('name')
    sql = '''SELECT id, name_enus FROM `tblDBCItem` WHERE name_enus LIKE "%{}%" '''.format(item_name)
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    if data:
        results = []
        for row in data:
            item = {}
            for tup in zip([column[0] for column in cursor.description], row):
                item[tup[0]] = tup[1]

            results.append(item)
    else:
        return jsonify({"error": "item not found"}), 404

    return jsonify({"items": results})

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    app.run(debug=True)
