from django.conf.urls import patterns, url


urlpatterns = patterns(
    'images.views',
    url(r'^not_listed/$', 'not_listed', name='not_listed'),
    url(r'^not_tagged/$', 'not_tagged', name='not_tagged'),
    url(r'^inappropriate/$', 'inappropriate', name='inappropriate'),
    url(r'^flag_inappropriate/(?P<unique_key>\w+)/$', 'flag_inappropriate', name='flag_inappropriate'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^(?P<unique_key>\w+)/$', 'detail', name='detail'),
)
