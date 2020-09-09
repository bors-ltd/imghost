from os.path import splitext
import random
import string

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from images.utils import create_thumb, identify_format


upload_path = "i/%Y/%m/"


class Image(models.Model):
    """A single image file."""

    unique_key = models.CharField(
        _("Unique key"), max_length=20, blank=True, unique=True
    )
    image = models.ImageField(
        _("Image file"),
        upload_to=upload_path,
        height_field="height",
        width_field="width",
    )
    thumb_small = models.ImageField(
        _("Small thumbnail"), blank=True, upload_to=upload_path
    )
    thumb_large = models.ImageField(
        _("Large thumbnail"), blank=True, upload_to=upload_path
    )
    extension = models.CharField(_("Extension"), max_length=5, blank=True, default="")
    height = models.PositiveIntegerField(_("Height"), blank=True, default=0)
    width = models.PositiveIntegerField(_("Width"), blank=True, default=0)
    source = models.URLField(_("Source"), max_length=2048, null=True, blank=True)

    is_meme = models.BooleanField(_("Is meme"), default=False)
    source_image = models.ForeignKey(
        "self",
        verbose_name=_("Source image"),
        related_name="related_memes",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

    listed = models.BooleanField(default=False, verbose_name=_("Listed"))

    inappropriate = models.BooleanField(default=False, verbose_name=_("Inappropriate"))

    tags = models.ManyToManyField(
        "images.Tag", blank=True, verbose_name=_("Tags"), related_name="tags"
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ("-created_on",)

    def __str__(self):
        return "%s%s" % (self.unique_key, self.extension)

    def get_absolute_url(self):
        return reverse("detail", args=[self.unique_key])

    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_unique_key()
            self.generate_extension()
            self.generate_image_filename()
            generate_thumbs = True
        else:
            generate_thumbs = False

        super(Image, self).save(*args, **kwargs)

        if generate_thumbs:
            self.generate_thumbnails()

    def get_unique_key(self):
        if not self.unique_key:
            self.generate_unique_key()

        return self.unique_key

    def generate_unique_key(self):
        key_chars = string.ascii_uppercase + string.digits
        self.unique_key = "".join(random.sample(key_chars, 10))

    def generate_extension(self):
        name, ext = splitext(self.image.url)
        if not ext:
            # Sniff extension from content
            ext = identify_format(self.image)
        self.extension = ext

    def generate_image_filename(self):
        image_name = "%s%s" % (self.unique_key, self.extension)
        self.image.name = image_name

    def generate_thumbnails(self):
        name = "%s_s%s" % (self.unique_key, self.extension)
        small_thumb = create_thumb(self.image, (150, 150))
        self.thumb_small.save(name, small_thumb)

        name = "%s_l%s" % (self.unique_key, self.extension)
        large_thumb = create_thumb(self.image, 700)
        self.thumb_large.save(name, large_thumb)


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ("name",)

    def __str__(self):
        return self.name
