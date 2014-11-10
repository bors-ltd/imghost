# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import json
import mimetypes

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from annoying.decorators import render_to

from images.models import Image
from memes.forms import MemeUploadForm


@require_GET
@render_to('meme.html')
def meme(request, unique_key):
    image = get_object_or_404(Image, unique_key=unique_key)
    mime = mimetypes.guess_type(image.image.url)[0]

    return {
        'image': image,
        'mime': mime,
    }


@require_POST
@permission_required('images.add_image', raise_exception=True)
@render_to("meme.html")
def create_meme(request):
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
            'errors': form.errors.get("__all__", ["Something went wrong. ‎(ﾉಥ益ಥ)ﾉ"]),
        })

    return HttpResponse(json_data, content_type="application/x-javascript")
