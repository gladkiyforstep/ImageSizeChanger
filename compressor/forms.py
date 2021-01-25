from django import forms
from compressor.models import Image, ChangedImage



class SimpleAddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('link', 'photo')
        labels = {
            'link': "Ссылка",
            'photo': "Файл"
        }


class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = ChangedImage
        fields = ('height', 'length')
        labels = {
            'height': "Высота",
            'length': "Ширина"
        }
