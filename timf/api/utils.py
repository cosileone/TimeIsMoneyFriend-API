#  Utilities
import decimal


def result_dictionary(cursor, data):
    item = {}
    for tup in zip([column[0] for column in cursor.description], data):
        x = tup[1]
        if isinstance(x, decimal.Decimal):
            x = float(x)
        item[tup[0]] = x

    return item
