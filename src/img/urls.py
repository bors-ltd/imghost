from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^images/', include('images.urls')),
    url(r'^memes/', include('memes.urls')),
    url(r'^legal_mentions/$', 'img.views.legal_mentions', name='legal_mentions'),
    url(r'^$', 'images.views.image_list', name='image_list'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
