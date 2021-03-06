from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('maps.urls')),
    url(r'^venue/', include('venues.urls')),
    url(r'^sightings/', include('sightings.urls')),

    # Examples:
    # url(r'^$', 'hoponit.views.home', name='home'),
    # url(r'^hoponit/', include('hoponit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
