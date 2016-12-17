from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin

import images.views
from img import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^images/', include('images.urls')),
    url(r'^memes/', include('memes.urls')),
    url(r'^legal_mentions/$', views.legal_mentions, name='legal_mentions'),
    url(r'^$', images.views.image_list, name='image_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
