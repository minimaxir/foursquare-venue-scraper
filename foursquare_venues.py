import yaml
import requests
import datetime

with open("config.yaml", "r") as f:
    cfg = yaml.load(f)

search_params = {
    'client_id': cfg['client_id'],
    'client_secret': cfg['client_secret'],
    'll': '{},{}'.format(cfg['top_bound'], cfg['bottom_bound']),
    'radius': 250,
    'limit': 50,
    'v': '20180218'
}

r = requests.get('https://api.foursquare.com/v2/venues/search',
                 params=search_params)
data = r.json()['response']

print(data)
