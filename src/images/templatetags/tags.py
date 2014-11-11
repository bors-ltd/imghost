# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import itertools

from django import template


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


@register.simple_tag()
def next_label():
    return label_sequence.next()
