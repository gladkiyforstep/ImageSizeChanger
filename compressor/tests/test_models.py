from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from compressor.models import Image


class ImageModelTest(TestCase):

    def test_bad_url(self):
        error = False
        img = Image(link='google')
        try:
            img.get_remote_image()
        except ValueError:
            error = True
        self.assertTrue(error)

    def test_good_url(self):
        error = False
        try:
            img = Image(link='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png')
            img.get_remote_image()
        except ValueError:
            error = True
        self.assertFalse(error)








