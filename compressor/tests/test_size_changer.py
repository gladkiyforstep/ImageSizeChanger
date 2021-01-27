from PIL import UnidentifiedImageError
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from compressor.SizeChanger import size_changer


class SizeChangerTest(TestCase):

    def test_not_image_file(self):
        error = False
        file = 'compressor/tests/google.txt'
        try:
            img = size_changer(file, height=100, length=100)
        except UnidentifiedImageError:
            error = True
        self.assertTrue(error)

    def test_bad_image_file(self):
        error = False
        file = 'compressor/tests/bad_img.jpg'
        try:
            img = size_changer(file, height=100, length=100)
        except UnidentifiedImageError:
            error = True
        self.assertTrue(error)

    def test_good_image_file(self):
        error = False
        file = 'compressor/tests/dean.jpg'
        try:
            img = size_changer(file, height=100, length=100)
        except:
            error = True
        self.assertFalse(error)

    def test_null_sizes(self):
        file = 'compressor/tests/dean.jpg'
        changed_image = size_changer(file, height=0, length=0)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        orig_image = Image.open(file)
        new_image = Image.open(changed_image_file)
        changed_image_file.flush()
        self.assertEqual(orig_image.size[0], new_image.size[0])

    def test_no_sizes(self):
        file = 'compressor/tests/dean.jpg'
        changed_image = size_changer(file)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        orig_image = Image.open(file)
        new_image = Image.open(changed_image_file)
        changed_image_file.flush()
        self.assertEqual(orig_image.size[0], new_image.size[0])

    def test_new_height_changed_both(self):
        file = 'compressor/tests/dean.jpg'
        height = 100
        width = 200
        changed_image = size_changer(file, height=height, length=width)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        new_image = Image.open(changed_image_file)
        changed_image_file.flush()
        self.assertEqual(height, new_image.size[1])

    def test_new_width_changed_both(self):
        file = 'compressor/tests/dean.jpg'
        height = 100
        width = 200
        changed_image = size_changer(file, height=height, length=width)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        new_image = Image.open(changed_image_file)
        changed_image_file.flush()
        self.assertEqual(width, new_image.size[0])

    def test_new_height_changed_only_height(self):
        file = 'compressor/tests/dean.jpg'
        height = 10
        changed_image = size_changer(file, height=height)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        new_image = Image.open(changed_image_file)
        changed_image_file.flush()
        self.assertEqual(height, new_image.size[1])

    def test_proportions_changed_only_height(self):
        file = 'compressor/tests/dean.jpg'
        height = 10
        changed_image = size_changer(file, height=height)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        orig_image = Image.open(file)
        orig_prop = float(orig_image.size[0])/float(orig_image.size[1])
        new_image = Image.open(changed_image_file)
        new_prop = float(new_image.size[0]) / float(new_image.size[1])
        changed_image_file.flush()
        self.assertEqual(int(orig_prop), int(new_prop))

    def test_new_width_changed_only_width(self):
        file = 'compressor/tests/dean.jpg'
        width = 15
        changed_image = size_changer(file, length=width)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        new_image = Image.open(changed_image_file)
        changed_image_file.flush()
        self.assertEqual(width, new_image.size[0])

    def test_proportions_changed_only_width(self):
        file = 'compressor/tests/dean.jpg'
        width = 15
        changed_image = size_changer(file, length=width)
        changed_image_file = InMemoryUploadedFile(
            changed_image,
            None,
            'resized.jpg',
            'image/jpeg',
            changed_image.tell,
            None
        )
        orig_image = Image.open(file)
        orig_prop = float(orig_image.size[0])/float(orig_image.size[1])
        new_image = Image.open(changed_image_file)
        new_prop = float(new_image.size[0]) / float(new_image.size[1])
        changed_image_file.flush()
        self.assertEqual(int(orig_prop), int(new_prop))
