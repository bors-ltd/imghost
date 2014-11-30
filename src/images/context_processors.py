# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from images import models


def inappropriate_counter(request):
    return {'inappropriate_counter': models.Image.objects.filter(inappropriate=True).count()}

