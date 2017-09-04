from __future__ import division
import wowapi
import urllib
import json
import time
import os

from run import app

BLIZZ_KEY = app.config['BLIZZ_KEY']
DEFAULT_SERVER = app.config['DEFAULT_REALM']
blizzapi = wowapi.API(BLIZZ_KEY)


class AuctionHouse(object):
    def __init__(self, server=DEFAULT_SERVER, download_data=False):
        self.server = server
        self.data = self.get_whole_ah(download_data)

    def get_whole_ah(self, save_file=False):
        # TODO: check new queries against last data retrieval
        auction_file = blizzapi.auction_status(self.server)
        data_url = auction_file['files'][0]['url']
        response = urllib.urlopen(data_url)
        auction_data = json.load(response)

        if save_file:
            self.save_json_to_disk(auction_data)
        print(data_url)

        return auction_data

    def save_json_to_disk(self, json_data):
        timestr = time.strftime("%Y.%m.%d-%H%M%S")
        dirname = "./Auction Data/%s/" % self.server
        filename = dirname + ("%s.json" % timestr)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, sort_keys=True, indent=4)

    def filter_by_item_id(self, item_id):
        results = []
        for auction in self.data['auctions']:
            if item_id == auction['item'] and auction['buyout']:
                results.append(auction)

        return results

    def calcStat(self, item_id, preferred_stat='min'):
        total_quantity = 0
        total_volume = 0
        mean_buyout = 0

        filtered_ah = self.filter_by_item_id(item_id)
        num_listings = len(filtered_ah)

        if num_listings > 0:
            min_buyout = filtered_ah[0]['buyout']

            for auction in filtered_ah:
                buyout = auction['buyout']
                quantity = auction['quantity']
                total_quantity += quantity
                total_volume += buyout
                min_buyout = min(min_buyout, (buyout/quantity))

            mean_buyout = total_volume / total_quantity

        results = {
            'auctions': num_listings,
            'total_quantity': total_quantity,
            'total_volume': total_volume/10000,
            'mean': mean_buyout/10000,
            'cheapest': min_buyout/10000
        }

        return results

