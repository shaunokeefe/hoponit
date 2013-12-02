from django.shortcuts import render
from django.views.generic import ListView

from venues.models import Beer, Venue

# Create your views here.

class BeerByVenueList(ListView):
    model = Beer
    template_name = 'sightings/beers_at_venue_list.html'
    context_object_name = 'beers'

    def get_queryset(self):
        venue_id = self.kwargs['venue_id']
        return Beer.objects.filter(sighting__venue__id=venue_id)


class VenuesWithBeerList(ListView):
    model = Venue
    template_name = 'sightings/venues_with_beer_list.html'
    context_object_name = 'venues'

    def get_queryset(self):
        beer_id = self.kwargs['beer_id']
        return Venue.objects.filter(sighting__beer__id=beer_id)
