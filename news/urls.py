from django.conf.urls import patterns, include, url

urlpatterns = patterns('news.views',
    url(r'^overview', 'overview', name='news_overview'),
    url(r'^(?P<slug>[\w\-]+)/$', 'detail', name='news_detail'),
#   next line to be used with URL-sorting
#    url(r'^archive/(?P<event_id>\d+)/$', 'archive', name='archive'),
    url(r'^archive', 'archive', name='news_archive'),
)
