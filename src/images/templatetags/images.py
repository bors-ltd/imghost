# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def full_img_url(context, url):
    request = context['request']
    return request.build_absolute_uri(url).replace("https://", "http://")
