from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from harvest import tasks

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        suburb = args[0]
        tasks.fetch(suburb=suburb)
        self.stdout.write('Succcess')
