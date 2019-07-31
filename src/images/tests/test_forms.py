from django.test import LiveServerTestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from images.forms import UploadForm


class UploadFormTests(LiveServerTestCase):
    def setUp(self):
        self.img_url = self.live_server_url + "/static/test_img.jpg"
        self.img_path = settings.BASE_DIR + "/static/test_img.jpg"
        self.upload_url = reverse("upload")

        self.test_img = SimpleUploadedFile(
            "test_img.jpg", bytes(self.img_path, "utf8"), content_type="image/jpeg"
        )

    def test_post_empty_form(self):
        data = {"url": ""}
        files = {"file": None}
        form = UploadForm(data, files)
        self.assertFalse(form.is_valid())

    def test_post_url(self):
        data = {"url": self.img_url}
        files = {"file": None}
        form = UploadForm(data, files)
        self.assertTrue(form.is_valid())

    def test_post_file(self):
        data = {"url": ""}
        files = {"file": self.test_img}
        form = UploadForm(data, files)
        self.assertTrue(form.is_valid())

    def test_post_both_url_and_file(self):
        data = {"url": self.img_url}
        files = {"file": self.test_img}
        form = UploadForm(data, files)
        self.assertFalse(form.is_valid())
