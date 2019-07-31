# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import itertools

from django import forms

from images import models


class UploadForm(forms.Form):
    url = forms.URLField(required=False)
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields["url"].widget.attrs["autocomplete"] = "off"

    def clean(self):
        data = super(UploadForm, self).clean()

        values = list(itertools.chain(data.values(), self.files.values()))
        if not any(values) or all(values):
            raise forms.ValidationError("Upload a file or give a url")

        return data


class ImageForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = models.Image
        fields = ("tags", "listed")

    def __init__(self, *args, **kwargs):
        if kwargs["instance"] and "new_tags" not in kwargs.setdefault("initial", {}):
            kwargs["initial"]["tags"] = "\r\n".join(
                kwargs["instance"].tags.values_list("name", flat=True)
            )
        super(ImageForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # First remove plain text tags that the model form could not handle
        tags = {name.strip() for name in self.cleaned_data.pop("tags").splitlines()}

        instance = super(ImageForm, self).save(*args, **kwargs)

        # Now create new tags and set the final list of tag instances
        tags = {
            models.Tag.objects.get_or_create(name__iexact=name)[0]
            for name in tags
            if name
        }
        instance.tags.set(tags)
