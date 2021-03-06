from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.crew.views',
    url(r'^$', 'crew', name='crew'),
    url(r'^rfid$', 'register_rfid', name='register_rfid'),
    url(r'^credit$', 'credit', name='credit'),
    url(r'^crewcard$', 'crewcard', name='crewcard'),
    url(r'^addcrew$', 'addcrewmember', name='addcrewmember'),
    url(r'^credit/overview$', 'credit_overview', name='credit_overview'),
    url(r'^(?P<crewteam_id>\d+)/$', 'crewteam', name='crewteam'),
    url(r'^application/overview', 'overview', name='application_overview'),
    url(r'^application/look/(?P<application_id>\d+)/$', 'look', name='look'),
    url(r'^application/user', 'user_overview', name='user_overview'),
    url(r'^application/new', 'new_application', name='new_application'),
    url(r'^application/edit/(?P<application_id>\d+)/$', 'new_application', name='edit_application'),
    url(r'^application/delete/(?P<application_id>\d+)/$', 'del_application', name='del_application'),

)
