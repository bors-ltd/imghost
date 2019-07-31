from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        auto_created=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unique_key",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        blank=True,
                        verbose_name="Unique key",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        height_field="height",
                        width_field="width",
                        upload_to="i/%Y/%m/",
                        verbose_name="Image file",
                    ),
                ),
                (
                    "thumb_small",
                    models.ImageField(
                        upload_to="i/%Y/%m/", blank=True, verbose_name="Small thumbnail"
                    ),
                ),
                (
                    "thumb_large",
                    models.ImageField(
                        upload_to="i/%Y/%m/", blank=True, verbose_name="Large thumbnail"
                    ),
                ),
                (
                    "extension",
                    models.CharField(
                        max_length=5, default="", blank=True, verbose_name="Extension"
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        default=0, blank=True, verbose_name="Height"
                    ),
                ),
                (
                    "width",
                    models.PositiveIntegerField(
                        default=0, blank=True, verbose_name="Width"
                    ),
                ),
                (
                    "source",
                    models.URLField(
                        max_length=2048, null=True, blank=True, verbose_name="Source"
                    ),
                ),
                ("is_meme", models.BooleanField(default=False, verbose_name="Is meme")),
                (
                    "created_on",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Created on"
                    ),
                ),
                ("listed", models.BooleanField(default=False, verbose_name="Listed")),
                (
                    "inappropriate",
                    models.BooleanField(default=False, verbose_name="Inappropriate"),
                ),
                (
                    "source_image",
                    models.ForeignKey(
                        to="images.Image",
                        null=True,
                        related_name="related_memes",
                        blank=True,
                        verbose_name="Source image",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_on",),
                "verbose_name_plural": "Images",
                "verbose_name": "Image",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        auto_created=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, unique=True)),
            ],
            options={
                "ordering": ("name",),
                "verbose_name_plural": "Tags",
                "verbose_name": "Tag",
            },
        ),
        migrations.AddField(
            model_name="image",
            name="tags",
            field=models.ManyToManyField(
                to="images.Tag", related_name="tags", blank=True, verbose_name="Tags"
            ),
        ),
    ]
