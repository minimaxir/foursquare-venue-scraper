import yaml
import requests
import datetime
import time


def get_intervals(lower, upper, length):
    # https://stackoverflow.com/a/6683724/9314418
    return([lower + x*(upper - lower)/length for x in range(length)])


with open("config.yaml", "r") as f:
    cfg = yaml.load(f)


lats = get_intervals(cfg['top_bound'], cfg['bottom_bound'], cfg['grid_size'])
longs = get_intervals(cfg['left_bound'], cfg['right_bound'], cfg['grid_size'])

search_params = {
    'client_id': cfg['client_id'],
    'client_secret': cfg['client_secret'],
    'radius': 250,
    'limit': 50,
    'v': '20180218'
}

venue_ids = set()

for lat in lats:
    for long in longs:
        search_params.update({'ll': '{},{}'.format(lat, long)})

        r = requests.get('https://api.foursquare.com/v2/venues/search',
                         params=search_params)
        venues = r.json()['response']['venues']

        for venue in venues:
            venue_ids.add(venue['id'])

        time.sleep(0.1)

print('{} Unique Venues Scraped.'.format(len(venue_ids)))
