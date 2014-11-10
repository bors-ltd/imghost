from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from images import models


class ImageAdmin(admin.ModelAdmin):
    list_display = ('unique_key', 'image', 'extension')
    actions = ['make_thumbnails']
    filter_horizontal = ('tags',)

    def make_thumbnails(self, request, queryset):
        for img in queryset:
            img.generate_thumbnails()
    make_thumbnails.short_description = _('Regenerates thumbnails')

admin.site.register(models.Image, ImageAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Tag, TagAdmin)
