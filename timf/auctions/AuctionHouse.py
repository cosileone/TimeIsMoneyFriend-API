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
    def __init__(self, region='US', server=DEFAULT_SERVER, download_data=False):
        blizzapi.region = region
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

    def read_json_from_disk(self):
        pass

    def save_json_to_disk(self, json_data):
        timestr = time.strftime("%Y.%m.%d-%H%M%S")
        dirname = "./Auction Data/{}/".format(self.server)
        filename = dirname + ("{}.json".format(timestr))

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, sort_keys=True, indent=4)

    def filter_by_item_ids(self, item_ids):
        results = []
        for auction in self.data['auctions']:
            if auction['item'] in item_ids:
                results.append(auction)

        return results

    def calcStats(self, item_ids):
        total_quantity = 0
        total_volume = 0
        mean_buyout = 0
        min_buyout = 0

        filtered_ah = self.filter_by_item_ids(item_ids)
        num_listings = len(filtered_ah)

        if num_listings > 0:
            min_bid = filtered_ah[0]['bid']

            for auction in filtered_ah:
                bid = auction['bid']
                quantity = auction['quantity']
                buyout = auction['buyout']
                if min_buyout == 0 and not buyout == 0:
                    min_buyout = buyout

                min_buyout = min(min_buyout, (buyout / quantity))
                min_bid = min(min_bid, (bid / quantity))

                total_quantity += quantity
                total_volume += buyout

            mean_buyout = total_volume / total_quantity
        else:
            min_bid = 0

        results = {
            'auctions': num_listings,
            'total_quantity': total_quantity,
            'total_volume': total_volume/10000,
            'mean_buyout': mean_buyout/10000,
            'cheapest_buyout': min_buyout/10000,
            'cheapest_bid': min_bid/10000
        }

        return results

