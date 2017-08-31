#  Utils


def result_dictionary(cursor, data):
    item = {}
    for tup in zip([column[0] for column in cursor.description], data):
        item[tup[0]] = tup[1]

    return item
