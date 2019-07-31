from django.conf.urls import url

from memes import views

urlpatterns = [
    url(
        r"^create/$", views.create_meme, name="create_meme"
    ),  # Before so 'create' does not match as a unique key
    url(r"^(?P<unique_key>\w+)/$", views.meme, name="meme"),
]
