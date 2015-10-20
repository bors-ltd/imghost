from io import BytesIO
from os.path import splitext
from os.path import basename

from PIL import Image, ImageOps

import requests

from django.core.files.images import ImageFile


def download_image(url):
    r = requests.get(url)
    name = basename(url)
    # Special case for Twitter, fuuuu
    if name.endswith(":large"):
        name = name[:-len(":large")]
    img_temp = BytesIO(r.content)
    image = ImageFile(img_temp, name=name)

    return image


def create_thumb(image, size):
    _basename, ext = splitext(image.name)
    ext = '.jpeg' if ext == '.jpg' else ext
    ext = ext[1:]

    thumbnail = Image.open(image.file.name)

    if type(size) == tuple:
        thumbnail = ImageOps.fit(thumbnail, size, Image.ANTIALIAS)
    else:
        thumbnail.thumbnail((size, size), Image.ANTIALIAS)

    tmp_file = BytesIO()
    thumbnail.save(tmp_file, ext)
    return ImageFile(tmp_file)
