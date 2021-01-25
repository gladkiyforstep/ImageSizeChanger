from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from django.db import models


class Image(models.Model):
    link = models.URLField(blank=True)
    photo = models.ImageField(upload_to='imgs', blank=True)

    def get_remote_image(self):
        if self.link and not self.photo:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.link).read())
            self.photo.save(f"{self.link[self.link.rfind('/')+1:]}", File(img_temp))
            img_temp.flush()
        self.save()


class ChangedImage(models.Model):
    height = models.IntegerField(blank=True)
    length = models.IntegerField(blank=True)
    photo = models.ImageField(upload_to='changed_imgs')
    not_changed_img = models.ForeignKey(Image, related_name='changed', on_delete=models.CASCADE)
