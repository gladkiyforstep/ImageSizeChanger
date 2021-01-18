from django import forms
from compressor.models import Image


class SimpleAddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'photo')
