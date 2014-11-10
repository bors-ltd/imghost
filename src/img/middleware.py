# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.sites.models import get_current_site


class CurrentSiteMiddleware(object):
    """
   Middleware that sets `site` attribute to request object.
   """
    def process_request(self, request):
        request.site = get_current_site(request)
