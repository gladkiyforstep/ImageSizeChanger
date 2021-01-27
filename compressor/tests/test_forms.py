from django.test import TestCase

from compressor.forms import SimpleAddImageForm


class SimpleAddImageFormTest(TestCase):

    def test_bad_url(self):
        form_data = {'link': 'google'}
        form = SimpleAddImageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_good_url(self):
        form_data = {'link': 'google.com'}
        form = SimpleAddImageForm(data=form_data)
        self.assertTrue(form.is_valid())

