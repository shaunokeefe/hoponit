from django.shortcuts import render
from django.views.generic import ListView

from .models import Venue


class VenueBySuburbList(ListView):
    model = Venue
    context_object_name = 'venues'

    def get_queryset(self):
        suburb_name = self.request.GET.get('suburb_name', None)
        return Venue.objects.filter(address__suburb=suburb_name)

    def get_context_data(self, **kwargs):
        context = super(VenueBySuburbList, self).get_context_data(**kwargs)
        context['suburb_name'] = self.request.GET.get('suburb_name', None)
        return context
