import googlemaps
from . import keys
api_key = keys.api_key

gm = googlemaps.Client(key = api_key)

def getLoc(address):
    geocode_result = gm.geocode(address)[0]
    return geocode_result['geometry']['location']