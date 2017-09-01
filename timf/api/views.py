from flask import jsonify, request

from . import api
from run import mysql
from utils import result_dictionary


@api.route('/items', methods=['GET'])
def list_items():
    sql = '''SELECT id, name_enus from tblDBCItem where auctionable = true;'''
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    results = []
    for row in data:
        item = result_dictionary(cursor, row)

        results.append(item)

    return jsonify({"items": results})


@api.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    sql = '''SELECT id, name_enus FROM tblDBCItem WHERE id = %s AND auctionable = true;'''
    cursor = mysql.connection.cursor()
    cursor.execute(sql, [item_id])
    data = cursor.fetchone()

    if data:
        item = result_dictionary(cursor, data)
    else:
        return jsonify({"error": "item not found"}), 404

    return jsonify(item)


@api.route('/item/', methods=['GET'])
def resolve_item_name():
    data = []
    query = request.args.get('name')

    if query:
        sql = '''SELECT id, name_enus FROM `tblDBCItem` WHERE name_enus LIKE %s;'''
        cursor = mysql.connection.cursor()
        cursor.execute(sql, ["%" + query + "%", ])
        data = cursor.fetchall()
    else:
        return jsonify({"error": "No item ID or query provided"}), 404

    if data:
        results = []
        for row in data:
            item = result_dictionary(cursor, row)

            results.append(item)
    else:
        return jsonify({"error": "item not found"}), 404

    return jsonify({"items": results})


@api.route('/realms', methods=['GET'])
def list_servers():
    sql = '''SELECT id, name, region, slug, population, house from tblRealm where region in ('US', 'EU');'''
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    results = []
    for row in data:
        item = result_dictionary(cursor, row)

        results.append(item)

    return jsonify({"realms": results})
