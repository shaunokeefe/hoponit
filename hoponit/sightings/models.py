from django.db import models
from django.contrib.auth import models as auth_models

#TODO (shauno): Change this to use explicit imports
from venues import models as venue_models

# Create your models here.

class Sighting(models.Model):
    when = models.DateTimeField()
    venue = models.ForeignKey(venue_models.Venue)
    beer = models.ForeignKey(venue_models.Beer)
    user = models.ForeignKey('User')

class User(models.Model):
    name = models.CharField(max_length="64")
    url = models.URLField()
    django_user = models.ForeignKey(auth_models.User, blank=True, null=True)
