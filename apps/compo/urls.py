from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.compo.views',
    url(r'^$', 'overview', name='overview'),
    url(r'^tournament/(?P<tournament_id>\d+)/$', 'tournament', name='tournament'),
    url(r'^tournament/join/(?P<tournament_id>\d+)/$', 'register_to_tournament', name='register_to_tournament'),

)
