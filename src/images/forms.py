from django import forms


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
