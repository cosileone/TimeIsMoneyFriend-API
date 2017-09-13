from run import sql_alchemy as db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(100), unique=True)

    # Possible options for fields:
    #  - blizz profile
    #  - character names
    #  - fav server
    #  - premium status (boolean/date?)
    #  - recipes
    #  - fav recipes
    #  - shopping list (item)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)
