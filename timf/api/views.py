from flask import jsonify, request

from . import api
from ..auctions.AuctionHouse import AuctionHouse
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
    query = request.args.get('realm')

    sql = '''SELECT id, name_enus FROM tblDBCItem WHERE id IN (%s) AND auctionable = true;'''
    cursor = mysql.connection.cursor()
    cursor.execute(sql, [item_id])
    data = cursor.fetchone()

    if data:
        item = result_dictionary(cursor, data)
    else:
        return jsonify({"error": "item not found"}), 404

    if query:
        ah = AuctionHouse(server=query)
        item['auction_data'] = ah.calcStats([item_id])

    return jsonify(item)


@api.route('/item/', methods=['GET'])
def resolve_item_name():
    data = []
    query = request.args.get('name')

    if query:
        # TODO: Paginate instead of LIMIT - http://flask.pocoo.org/snippets/44/
        sql = '''SELECT id, name_enus FROM `tblDBCItem` WHERE name_enus LIKE %s AND auctionable = true LIMIT 25;'''
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
