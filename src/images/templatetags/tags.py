# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import itertools

from django import template
from django.db import models

from images import models as images_models


register = template.Library()


ALL_LABELS = (
    "label label-default",
    "label label-primary",
    "label label-success",
    "label label-info",
    "label label-warning",
    "label label-danger",
)

label_sequence = itertools.cycle(ALL_LABELS)


@register.inclusion_tag("snippets/tags.html")
def show_tags(tags=None):
    if tags is None:
        tags = images_models.Tag.objects.annotate(count=models.Count('tags'))
    else:
        tags = tags.annotate(count=models.Count('tags'))

    annotated_tags = []
    for tag in tags:
        tag.font_size = "%d%%" % (75 + 10 * getattr(tag, 'count', 0))
        tag.css_class = label_sequence.next()
        annotated_tags.append(tag)

    return {
        'tags': annotated_tags,
    }
