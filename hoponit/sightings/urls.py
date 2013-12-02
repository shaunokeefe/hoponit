from django.conf.urls import patterns, include, url

from .views import BeerByVenueList, VenuesWithBeerList

urlpatterns = patterns('',
    url(r'^beers/(?P<venue_id>\d+)/$', BeerByVenueList.as_view(), name='beer-by-venue-list'),
    url(r'^venues/(?P<beer_id>\d+)/$', VenuesWithBeerList.as_view(), name='beer-by-venue-list'),
)
