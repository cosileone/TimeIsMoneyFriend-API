# Statement for enabling the development environment
DEBUG = False
DOWNLOAD_DATA = True

MYSQL_HOST = 'newswire.theunderminejournal.com'
MYSQL_DB = 'newsstand'

DEFAULT_REALM = 'malganis'

SQLALCHEMY_DATABASE_URI = 'postgres://localhost/timf'

SQLALCHEMY_BINDS = {
    'newsstand': 'mysqldb://newswire.theunderminejournal.com/newsstand',
}