import atexit
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler

job_defaults = {
    'max_instances': 247  # number of Auction Houses
}

scheduler = BackgroundScheduler()

# add jobs here
@scheduled_job()
def getAuctionHouse():
    pass

scheduler.configure(job_defaults=job_defaults, timezone=utc)
