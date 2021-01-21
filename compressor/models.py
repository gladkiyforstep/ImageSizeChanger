from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='imgs')


class ChangedImage(models.Model):
    height = models.IntegerField(blank=True)
    length = models.IntegerField(blank=True)
    photo = models.ImageField(upload_to='changed_imgs')
    not_changed_img = models.ForeignKey(Image, related_name='changed', on_delete=models.CASCADE)
