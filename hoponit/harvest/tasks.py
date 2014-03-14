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
    suburb_unique_beers = {}
    suburb_unique_beer_locations = {}

    for venue in venues:
        venue_json = venue
        checkins = untappd.get_venue_checkins(foursquare_venue_id=venue['id'])
        if not checkins:
            continue
        venue_json['checkins'] = checkins
        venue_unique_beers = {}
        for checkin in checkins:
            bid = str(checkin['beer']['bid'])
            venue_unique_beers[bid] = checkin['beer']
            suburb_unique_beers[bid] = checkin['beer']
            if not bid in  suburb_unique_beer_locations:
                suburb_unique_beer_locations[bid] = []
            suburb_unique_beer_locations[bid].append(venue)

        venue_json['unique_beers'] = venue_unique_beers
        suburb_json['venues'].append(venue_json)
        suburb_json['unique_beers'] = suburb_unique_beers
        suburb_json['unique_beer_locations'] = suburb_unique_beer_locations

    mongo_client.hoponit.suburbs.insert(suburb_json)
    return suburb_json


def fetch_task(suburb='Northcote'):
    fetch(suburb=suburb)
