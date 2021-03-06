from django import template
from django.conf import settings
from django.urls import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def secure_url(context, url):
    if isinstance(url, str):
        url = reverse(url)
    url = context["request"].build_absolute_uri(url)
    if settings.SESSION_COOKIE_SECURE:
        url = url.replace("http://", "https://")
    return url
