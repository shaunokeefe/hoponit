from django.conf import settings
from django.shortcuts import render_to_response

import foursquare
from hammock import Hammock as Untappd
from pymongo import MongoClient


class NotCachedException(Exception):
    pass

def _check_limit():
    u = Untappd('http://api.untappd.com/v4')
    client_key = settings.UNTAPPD_CLIENT_KEY
    client_secret = settings.UNTAPPD_CLIENT_SECRET
    response = u.venue.checkins(None).GET(params={'client_id': client_key, 'client_secret': client_secret})
    print response.headers['x-ratelimit-remaining']

def _venues_for_suburb(suburb):
        foursquare_client = foursquare.Foursquare(client_id=settings.FOURSQUARE_CLIENT_ID, client_secret=settings.FOURSQUARE_CLIENT_SECRET, redirect_uri='')
        venues = foursquare_client.venues.search(params={'near': suburb})['venues']
        return venues

def _checkins_for_suburb(suburb):
        foursquare_client = foursquare.Foursquare(client_id=settings.FOURSQUARE_CLIENT_ID, client_secret=settings.FOURSQUARE_CLIENT_SECRET, redirect_uri='')
        venues = foursquare_client.venues.search(params={'near': suburb})['venues']
        return venues

def _get_beers(client, venue_name):
    beers = client.hoponit.beers.find_one({'venue': venue_name})
    if not beers:
        raise NotCachedException()
    return beers['beers']


def get_venues(request):

    suburb = request.GET.get('suburb_name', None)
    if not suburb:
        return render_to_response("maps/main_map.html", {})

    mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

    # Try getting the foursquare info from mongo first
    venues = None
    mongo_response = mongo_client.hoponit.venues.find_one({'suburb': suburb})
    if mongo_response:
        venues = mongo_response.get('venues', None)

    if not venues:
        # Venues not in mongo. Get list of venues in suburb from Foursquare
        foursquare_client = foursquare.Foursquare(client_id=settings.FOURSQUARE_CLIENT_ID, client_secret=settings.FOURSQUARE_CLIENT_SECRET, redirect_uri='')
        venues = _venues_for_suburb(suburb)
        mongo_client.hoponit.venues.insert({'suburb': suburb, 'venues': venues})

    venue_names = set()
    beer_names = set()
    all_beers = []
    venues_and_beers = []

    u = Untappd('http://api.untappd.com/v4')
    client_key = settings.UNTAPPD_CLIENT_KEY
    client_secret = settings.UNTAPPD_CLIENT_SECRET

    for venue in venues:
        try:
            # Try getting the untappd info from mongo first
            beers = _get_beers(mongo_client, venue['name'])
            if beers:
                venue_names.add(venue['name'])
                venues_and_beers.append({'venue': venue['name'], 'beers': beers})
        except NotCachedException:
            untappd_response = u.venue.foursquare_lookup(venue['id']).GET(params={'client_id': client_key, 'client_secret': client_secret}).json()['response']
            if not untappd_response:
                mongo_client.hoponit.beers.insert({'venue': venue['name'], 'beers': []})
                continue
            beers = []
            for untappd_venue in untappd_response['venue']['items']:
                checkins = u.venue.checkins(untappd_venue['venue_id']).GET(params={'client_id': client_key, 'client_secret': client_secret}).json()['response']['checkins']['items']
                if checkins:
                    venue_names.add(untappd_venue['name'])
                for checkin in checkins:
                    beers.append(checkin['beer'])
                    beer_names.add(checkin['beer']['beer_name'])

                venues_and_beers.append({'venue': venue['name'], 'beers': beers})
                mongo_client.hoponit.beers.insert({'venue': venue['name'], 'beers': beers})
        all_beers.extend(beers)

    print "Beers ", list(all_beers)
    print "Venues",  list(venue_names)
    values_dict = {'suburb': suburb, 'venues': venues_and_beers}

    return render_to_response("maps/main_map.html", values_dict)
