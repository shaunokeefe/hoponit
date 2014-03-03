import foursquare
import requests
from pymongo import MongoClient

from django.conf import settings


class InvalidParameterException(Exception):
    pass


class UntappdApiError(Exception):
    pass


class UntappdApi(object):

    def __init__(self, endpoint, client_id=None, client_secret=None):

        if client_id is None:
            client_id = settings.HARVEST_UNTAPPD_CLIENT_ID
        if client_secret is None:
            client_secret = settings.HARVEST_UNTAPPD_CLIENT_SECRET
        if endpoint is None:
            endpoint = settings.HARVEST_UNTAPPD_CLIENT_SECRET

        self.client_id = client_id
        self.client_secret = client_secret
        self.api_endpoint = endpoint
        self.credentials = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
            }

    def _request(self, path, id):
        url = "%s/%s%s" % (self.api_endpoint, path, id)
        response = requests.get(url, params=self.credentials)
        response_json = response.json()
        if not response.status_code == 200:
            meta = response_json['meta']
            raise UntappdApiError(meta['error_type'] + ': ' + meta['error_detail'])
        return response_json['response'], response_json['meta']

    def get_venue_checkins(self, venue_id=None, foursquare_venue_id=None):
        if not venue_id and not foursquare_venue_id:
            raise InvalidParameterException()

        if not venue_id and foursquare_venue_id:
            venue = self.foursquare_id_to_untappd(foursquare_venue_id)
            if not venue:
                return None

            venue_id = venue['venue_id']

        url = 'venue/checkins/'
        response, meta = self._request(url, venue_id)
        return response['checkins']['items']

    def foursquare_id_to_untappd(self, venue_foursquare_id):
        path = 'venue/foursquare_lookup/'
        try:
            response, meta = self._request(path, venue_foursquare_id)
        except UntappdApiError:
            return None
        #untappd_venue_id = response['venue']['items'][0]['venue_id']
        untappd_venue = response['venue']['items'][0]
        return untappd_venue

    def get_venue(self, venue_id):
        path = 'venue/'
        try:
            response, meta = self._request(path, venue_id)
        except UntappdApiError:
            return None
        return response

    def get_venues_for_suburb(self, suburb):
        foursquare_client = foursquare.Foursquare(
            client_id=settings.HARVEST_FOURSQUARE_CLIENT_ID,
            client_secret=settings.HARVEST_FOURSQUARE_CLIENT_SECRET,
            redirect_uri=''
        )
        venues = foursquare_client.venues.search(params={'near': suburb})['venues']
        return venues

    def check_limit(self):
        response, meta = self._request('', None)
        return response.headers['x-ratelimit-remaining']
