import yaml
import requests
import datetime
import time
import csv

# Get all Venue IDs for venues within the bounding box.


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

print('{} Unique Venues Scraped: {}.'.format(
    len(venue_ids), datetime.datetime.now()))

# Get and process the data for each unique Venue.

venue_params = {
    'client_id': cfg['client_id'],
    'client_secret': cfg['client_secret'],
    'v': '20180218'
}

venue_ids_list = list(venue_ids)   # cannot iterate a set, so must coerce list
venue_count = 0

with open('foursquare_venues.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'categories', 'lat', 'long', 'num_checkins',
                     'num_likes', 'price', 'rating',
                     'num_ratings', 'url_venue', 'url_foursquare'])

    for venue_id in venue_ids_list:
        r = requests.get(
            'https://api.foursquare.com/v2/venues/{}'.format(venue_id),
            params=venue_params)

        if 'venue' in r.json()['response']:
            venue = r.json()['response']['venue']

            id = venue_id
            name = venue.get('name', '')
            lat = venue.get('location', {}).get('lat', '')
            long = venue.get('location', {}).get('lng', '')
            num_checkins = venue.get('stats', {}).get('checkinsCount', '')
            num_likes = venue.get('likes', {}).get('count', '')
            rating = venue.get('rating', '')
            num_ratings = venue.get('ratingSignals', '')
            price = venue.get('price', {}).get('tier')
            url_venue = venue.get('url', '')
            url_foursquare = venue.get('shortUrl', '')

            # categories is an empty list if there are none.
            categories = venue.get('categories', '')
            if len(categories) == 0:
                categories = ''
            else:
                categories = ', '.join([x['name'] for x in categories])

            writer.writerow([id, name, categories, lat, long, num_checkins,
                             num_likes, price, rating,
                             num_ratings, url_venue, url_foursquare])

            venue_count += 1

            if venue_count % 1000 == 0:
                print('{} Retrieved: {}'.format(venue_count,
                                                datetime.datetime.now()))

        time.sleep(0.1)
