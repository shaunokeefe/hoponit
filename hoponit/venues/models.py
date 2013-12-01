from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.

class Address(models.Model):
    name = models.CharField(max_length="64")
    street_number = models.IntegerField()
    apt_number = models.IntegerField(null=True, blank=True)
    suburb = models.CharField(max_length="64")
    state = models.CharField(max_length=3)
    postcode = models.IntegerField()

class Venue(models.Model):
    PUB = 1
    RESTAURANT = 2
    TRUCK = 3

    VENUE_TYPE_CHOICES = (
    (PUB, 'Pub'),
    (RESTAURANT, 'Restaurant'),
    (TRUCK, 'Truck'),
)
    name = models.CharField(max_length="64")
    closing = models.TimeField()
    opening = models.TimeField()
    type = models.IntegerField(choices=VENUE_TYPE_CHOICES)
    address = models.ForeignKey('Address')

class Beer(models.Model):
    name = models.CharField(max_length="64")
    type = models.ManyToManyField('BeerType')

class BeerType(models.Model):
    name = models.CharField(max_length="64")
