from django.conf.urls import patterns, url


urlpatterns = patterns(
    'memes.views',
    url(r'^create/$', 'create_meme', name='create_meme'),  # Before so 'create' does not match as a unique key
    url(r'^(?P<unique_key>\w+)/$', 'meme', name='meme'),
)
