from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Venue)
admin.site.register(models.Address)
admin.site.register(models.Beer)
admin.site.register(models.BeerType)
