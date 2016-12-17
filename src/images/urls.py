from django.conf.urls import url

from images import views


urlpatterns = [
    url(r'^not_listed/$', views.not_listed, name='not_listed'),
    url(r'^not_tagged/$', views.not_tagged, name='not_tagged'),
    url(r'^inappropriate/$', views.inappropriate, name='inappropriate'),
    url(r'^flag_inappropriate/(?P<unique_key>\w+)/$', views.flag_inappropriate, name='flag_inappropriate'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^(?P<unique_key>\w+)/$', views.detail, name='detail'),
]
