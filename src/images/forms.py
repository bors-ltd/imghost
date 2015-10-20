# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import itertools

from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from images import models


class UploadForm(forms.Form):
    url = forms.URLField(required=False)
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['autocomplete'] = "off"

    def clean(self):
        data = super(UploadForm, self).clean()

        values = list(itertools.chain(data.values(), self.files.values()))
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


class ImageForm(forms.ModelForm):
    new_tags = forms.CharField(
        label=_(u"New tags"), required=False, widget=forms.Textarea({'rows': '1', 'class': "form-control"}))

    class Meta:
        model = models.Image
        fields = ('tags', 'new_tags', 'listed')
        widgets = {
            'tags': CheckboxSelectMultiple,
        }

    def clean_new_tags(self):
        new_tags = set()
        for new_tag in self.cleaned_data['new_tags'].splitlines():
            new_tag = new_tag.strip()
            if new_tag:
                new_tags.add(new_tag)
        return new_tags

    def save(self, *args, **kwargs):
        instance = super(ImageForm, self).save(*args, **kwargs)
        for new_tag in self.cleaned_data['new_tags']:
            instance.tags.add(models.Tag.objects.get_or_create(name=new_tag)[0])
