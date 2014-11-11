# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import itertools

from django import forms
from django.template.loader import render_to_string

from images import models


class UploadForm(forms.Form):
    url = forms.URLField(required=False)
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['autocomplete'] = "off"

    def clean(self):
        data = super(UploadForm, self).clean()

        values = data.values() + self.files.values()
        if not any(values) or all(values):
            raise forms.ValidationError('Upload a file or give a url')

        return data


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = self._empty_value
        final_attrs = self.build_attrs(attrs)
        choices = list(itertools.chain(self.choices, choices))
        return render_to_string("snippets/checkbox_select_multiple.html", {
            'name': name,
            'value': value,
            'attrs': final_attrs,
            'choices': choices,
        })


class TagsForm(forms.ModelForm):

    class Meta:
        model = models.Image
        fields = ('tags',)
        widgets = {
            'tags': CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super(TagsForm, self).clean()
        return cleaned_data
