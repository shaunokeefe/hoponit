from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from maps.views import get_venues

urlpatterns = patterns('',
    #url(r'^$', VenueBySuburbList.as_view(template_name="maps/main_map.html"),
    #    name='map-search'),
    url(r'^$', get_venues, name='map-search'),
)
