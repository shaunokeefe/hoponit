from django.conf import settings
from django.shortcuts import render_to_response

import foursquare
from hammock import Hammock as Untappd
from pymongo import MongoClient


class NotCachedException(Exception):
    pass


def get_venues(request):

    suburb_name = request.GET.get('suburb_name', None)
    if not suburb_name:
        return render_to_response("maps/main_map.html", {})

    mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

    # Try getting the foursquare info from mongo first
    venues = None
    mongo_response = mongo_client.hoponit.suburbs.find_one({'_id': suburb_name})
    if mongo_response:
        venues = mongo_response.get('venues', None)

    values_dict = {'suburb_name': suburb_name, 'venues': venues}

    return render_to_response("maps/main_map.html", values_dict)
