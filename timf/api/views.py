from flask import jsonify, request
from collections import defaultdict

from . import api
from ..auctions.AuctionHouse import AuctionHouse
from run import mysql
from utils import result_dictionary


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
    region = request.args.get('region')
    realm = request.args.get('realm')

    sql = '''SELECT id, name_enus FROM tblDBCItem WHERE id IN (%s) AND auctionable = true;'''
    cursor = mysql.connection.cursor()
    cursor.execute(sql, [item_id])
    data = cursor.fetchone()

    if data:
        item = result_dictionary(cursor, data)
    else:
        return jsonify({"error": "item not found"}), 404

    if realm:
        if region:
            ah = AuctionHouse(region=region, server=realm, download_data=True)
        else:
            ah = AuctionHouse(server=realm)
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


@api.route('/recipe/<string:item_name>', methods=['GET'])
def get_recipes(item_name):
    region = request.args.get('region')
    realm = request.args.get('realm')

    sql = '''SELECT spells.id,
                    spells.name AS recipe,
                    tradeskills.name AS tradeskill,
                    items.id AS reagent_id,
                    items.name_enus AS reagent,
                    reagents.quantity
            FROM `tblDBCItemReagents` AS reagents
            INNER JOIN tblDBCItem AS items
                ON reagent = items.id
            INNER JOIN tblDBCSpell AS spells
                ON spell = spells.id
            INNER JOIN tblDBCSkillLines AS tradeskills
                ON reagents.skillline = tradeskills.id
            WHERE spells.name LIKE %s
            OR items.name_enus LIKE %s
            AND spells.skillline IS NOT NULL;
           '''
    cursor = mysql.connection.cursor()
    likestring = "%" + item_name + "%"
    cursor.execute(sql, [likestring, likestring])
    data = cursor.fetchall()

    if data:
        results = {}
        for row in data:
            try:
                reagents = results[row[1]]['reagents']
            except KeyError:
                reagents = []
            reagents.append({
                'id': row[3],
                'reagent': row[4],
                'quantity': float(row[5]),
            })

            recipe = {
                'id': row[0],
                'name': row[1],
                'tradeskill': row[2],
                'reagents': reagents
            }

            results[row[1]] = recipe

    else:
        return jsonify({"error": "no recipes found"}), 404

    if realm:
        if region:
            # ah = Recipe(region=region, server=realm, download_data=True)
            pass
        else:
            # ah = Recipe(server=realm)
            pass
        # recipe['auction_data'] = ah.calcStats([item_name])

    return jsonify({"count": len(results), "recipes": results.values()})
