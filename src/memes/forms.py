import base64
from io import BytesIO
import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile

from images.models import Image


class MemeUploadForm(forms.Form):
    source_image = forms.ModelChoiceField(Image.objects.all())
    file = forms.CharField()
    mime = forms.CharField()
    top_text = forms.CharField(required=False)
    bottom_text = forms.CharField(required=False)

    def clean_file(self):
        data = self.cleaned_data["file"]
        matches = re.search(r"base64,(.*)", data)
        imgstr = matches.group(1)
        imgcontent = BytesIO(base64.b64decode(imgstr))
        img = ImageFile(imgcontent, name="temp.png")

        return img

    def clean(self):
        cleaned_data = super(MemeUploadForm, self).clean()
        if not cleaned_data["top_text"] and not cleaned_data["bottom_text"]:
            raise ValidationError("WHY U NO TYPE TEXT ლ(ಠ益ಠლ)")
        return cleaned_data
