from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from harvest import untappd

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        cmd = args[0]
        u = untappd.UntappdApi(settings.HARVEST_UNTAPPD_CLIENT_ENDPOINT)

        if cmd == "venue":
            venue_id = args[1]
            venue = u.foursquare_id_to_untappd(venue_id)

        if cmd == "fs":
            venue_id = args[1]
            venue = u.foursquare_id_to_untappd(venue_id)
            print venue

        if cmd == "checkins":
            venue_id = args[1]
            checkins = u.get_venue_checkins(venue_id=venue_id)
            for checkin in checkins:
                print "%s" % (checkin)

        if cmd == "fscheckins":
            venue_id = args[1]
            checkins = u.get_venue_checkins(foursquare_venue_id=venue_id)
            for checkin in checkins:
                print "%s" % (checkin)

        if cmd == "limit":
            print check_limit()

        if cmd == "suburb":
            suburb = args[1]
            venues = u.get_venues_for_suburb(suburb)
            for venue in venues:
                print "%s: %s" % (venue['id'], venue['name'])

        self.stdout.write('Succcess')
