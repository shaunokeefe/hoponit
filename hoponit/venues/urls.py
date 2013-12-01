from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView

from .models import Venue

urlpatterns = patterns('',#'venues.views',
    url(r'^$', ListView.as_view(model=Venue, context_object_name='venues'), name='venue-list'),
    #url(r'^add/$', 'idea_add', name='idea-create'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Venue, context_object_name='venue'), name='venue-detail'),
    #url(r'^(?P<idea_id>\d+)/$', 'venue_detail', name='venue-detail'),
    #url(r'^(?P<idea_id>\d+)/up/$', 'idea_vote', {'direction': 1}, name='idea-vote-up'),
    #url(r'^(?P<idea_id>\d+)/down/$', 'idea_vote', {'direction': -1}, name='idea-vote-down'),
    #url(r'^(?P<idea_id>\d+)/comment/$', 'idea_comment', name='idea-comment'),
)

