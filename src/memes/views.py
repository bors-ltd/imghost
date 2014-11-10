import mimetypes
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from annoying.decorators import render_to

from images.models import Image
from memes.forms import MemeUploadForm


@render_to('meme.html')
def meme(request, unique_key):
    image = get_object_or_404(Image, unique_key=unique_key)
    mime = mimetypes.guess_type(image.image.url)[0]

    if request.method == 'POST':
        form = MemeUploadForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            img = Image.objects.create(
                image=data['file'],
                source='',
                extension='png',
                is_meme=True,
                source_image=data['source_image']
            )

            json_data = json.dumps({
                'redirect': img.get_absolute_url()
            })
        else:
            json_data = json.dumps({
                'errors': form.errors["__all__"],
            })
        return HttpResponse(json_data, content_type="application/x-javascript")

    return {
        'image': image,
        'mime': mime,
    }
