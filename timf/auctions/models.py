from run import sql_alchemy as db


class Realm(db.Model):
    auctionhouse_id = db.column(db.Integer, db.ForeignKey('auction_house.house'))


class AuctionHouse(db.Model):
    house = db.Column(db.integer, primary_key=True)

    lastcheck = db.Column(db.DateTime)
    lastchecksuccess = db.Column(db.DateTime)
    lastchecksuccessresult = db.Column(db.String)

    file = db.column(db.String(50))

    realm_id = db.column(db.Integer, db.ForeignKey('realm.id'))
    realm = db.relationship(
        'Realm',
        backref=db.backref('auction_house', lazy='dynamic')
    )

    latest = db.column(db.LargeBinary)


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey)
    auction_data = db.ForeignKey()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
