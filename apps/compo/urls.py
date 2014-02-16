from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.compo.views',
    url(r'^$', 'overview', name='tournament_overview'),
    url(r'^tournament/(?P<tournament_id>\d+)/$', 'tournament', name='tournament'),
    url(r'^tournament/join/(?P<tournament_id>\d+)/$', 'register_to_tournament', name='register_to_tournament'),
    url(r'^tournament/check/(?P<tournament_id>\d+)/$', 'check_user', name='check_user'),
    url(r'^tournament/remove/(?P<tournament_id>\d+)/$', 'remove_participant', name='remove_participant'),

)