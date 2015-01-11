# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from annoying.decorators import render_to

from images import forms
from images import models
from images.utils import download_image


@permission_required('images.add_image')
@render_to('upload.html')
def upload(request):
    form = forms.UploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            url = form.cleaned_data['url']
            file = form.cleaned_data['file']
            image_file = file if file else download_image(url)

            image = models.Image.objects.create(
                image=image_file,
                source=url or '',
            )

            return redirect(image.get_absolute_url())

        else:
            messages.error(request, _("Please check the errors below."))

    return {
        'form': form,
    }


@render_to('list.html')
def image_list(request):
    images = models.Image.objects.filter(listed=True, is_meme=False)

    tag_list = request.GET.getlist('tags')
    if tag_list:
        images = images.filter(tags__name__in=tag_list)

    search_query = request.GET.get('q', "").strip()
    if search_query:
        images = images.filter(tags__name__icontains=search_query)

    return {
        'images': images,
        'tags': models.Tag.objects.all(),
        'form': forms.UploadForm(),
    }


@permission_required('images.change_image')
@render_to('list.html')
def not_listed(request):
    images = models.Image.objects.filter(listed=False, is_meme=False)

    return {'images': images}


@permission_required('images.change_image')
@render_to('list.html')
def not_tagged(request):
    images = models.Image.objects.filter(tags__isnull=True, is_meme=False)

    return {'images': images}


@permission_required('images.delete_image')
@render_to('list.html')
def inappropriate(request):
    images = models.Image.objects.filter(inappropriate=True)

    return {'images': images}


@render_to('detail.html')
def detail(request, unique_key):
    image = get_object_or_404(models.Image, unique_key=unique_key)

    form = forms.ImageForm(data=request.POST or None, instance=image)

    if image.is_meme:
        base_key = image.source_image.unique_key
    else:
        base_key = image.unique_key

    if request.method == 'POST' and request.user.has_perm('images.change_image'):
        if form.is_valid() :
            form.save()
            messages.success(request, _("Image updated successfully."))

            return HttpResponseRedirect(image.get_absolute_url())

        else:
            messages.error(request, _("Please check the errors below."))

    return {
        'unique_key': unique_key,
        'image': image,
        'form': form,
        # For memes
        'base_key': base_key,
        'related_memes': image.related_memes.all(),
        'has_memes': len(image.related_memes.all()) > 0,
    }


@require_POST
def flag_inappropriate(request, unique_key):
    image = get_object_or_404(models.Image, unique_key=unique_key)
    image.inappropriate = True
    image.save(update_fields=['inappropriate'])

    messages.success(
      request, _("This image was successfully flagged as inappropriate. We will soon investigate further.")
    )

    return HttpResponseRedirect(image.get_absolute_url())
