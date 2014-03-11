import pprint
from optparse import make_option
from pymongo import MongoClient

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from harvest import tasks

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'
    option_list = BaseCommand.option_list + (
    make_option('--venue',
        action='store_true',
        dest='venue',
        default=None,
        help=''),
    )


    def handle(self, *args, **options):
        suburb_name = args[0]
        mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        mongo_response = mongo_client.hoponit.suburbs.find_one({'_id': suburb_name})
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(mongo_response)
        self.stdout.write('Succcess')
