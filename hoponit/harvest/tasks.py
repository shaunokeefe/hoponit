from pymongo import MongoClient

from django.conf import settings

from .untappd import UntappdApi


def fetch(suburb='Northcote'):
    untappd = UntappdApi(
        settings.HARVEST_UNTAPPD_CLIENT_ENDPOINT,
        client_id = settings.HARVEST_UNTAPPD_CLIENT_ID,
        client_secret = settings.HARVEST_UNTAPPD_CLIENT_SECRET
    )

    venues = untappd.get_venues_for_suburb(suburb)

    mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    mongo_client.hoponit.suburbs.remove({'_id': suburb})

    suburb_json = {'_id': suburb}
    suburb_json['venues'] = []
    for venue in venues:
        venue_json = venue
        checkins = untappd.get_venue_checkins(foursquare_venue_id=venue['id'])
        if not checkins:
            continue
        venue_json['checkins'] = checkins
        suburb_json['venues'].append(venue_json)

    mongo_client.hoponit.suburbs.insert(suburb_json)
    return suburb_json


def fetch_task(suburb='Northcote'):
    fetch(suburb=suburb)

#def process_venue(suburb, foursquare_venue):
#    foursquare_venue_id = foursquare_venue['id']
#    checkins = untappd.get_venue_checkins(foursquare_venue_id=foursquare_venue_id)
#
#    if checkins:
#        mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
#
#        # Try getting the foursquare info from mongo first
#        venue = None
#        mongo_response = mongo_client.hoponit.venues.find_one({'suburb': suburb})
#        save_venue(suburb, foursquare_venue)
#        save_checkins(suburb, foursquare_venue, checkins)
#
#def save_venue(suburb, venue):
#    mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
#
#    # Try getting the foursquare info from mongo first
#    venue = None
#    mongo_response = mongo_client.hoponit.venues.find_one({'suburb': suburb})
#    if mongo_response:
#        venues = mongo_response.get('venues', None)
#
#    mongo_client.hoponit.venues.insert({'suburb': suburb, 'venues': venues})
#
#def save_checkins(suburb, venue, checkins):
#    pass
