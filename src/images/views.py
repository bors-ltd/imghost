# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from annoying.decorators import render_to

from images import forms
from images import models
from images.utils import download_image


@render_to('upload.html')
def upload(request):

    if not request.user.is_authenticated():
        raise PermissionDenied('Sorry, only the keymaster can do this.')

    form = forms.UploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():

        url = form.cleaned_data['url']
        file = form.cleaned_data['file']
        image_file = file if file else download_image(url)

        image = models.Image.objects.create(
            image=image_file,
            source=url or '',
        )

        return redirect(image.get_absolute_url())

    return {
        'form': form,
    }


@render_to('list.html')
def list(request):
    images = models.Image.objects.filter(is_meme=False)

    tag_list = request.GET.getlist('tags')
    if tag_list:
        images = images.filter(tags__name__in=tag_list)

    tags = models.Tag.objects.all()

    form = forms.UploadForm()

    return {
        'images': images,
        'tags': tags,
        'form': form,
    }


@render_to('detail.html')
def detail(request, unique_key):
    image = get_object_or_404(models.Image, unique_key=unique_key)

    form = forms.ImageForm(data=request.POST or None, instance=image)

    if image.is_meme:
        base_key = image.source_image.unique_key
    else:
        base_key = image.unique_key

    if request.method == 'POST' and form.is_valid() and request.user.has_perm('images.change_image'):
        form.save()
        return HttpResponseRedirect(image.get_absolute_url())

    return {
        'image': image,
        'form': form,
        # For memes
        'base_key': base_key,
        'related_memes': image.related_memes.all(),
        'has_memes': len(image.related_memes.all()) > 0,
    }
