from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def size_changer(file, height=0, length=0):
    img = Image.open(file)
    img_format = file.name[file.name.rfind('.')+1:]
    resized_img = img
    if height != 0 and length != 0:
        resized_img = img.resize((length, height), Image.ANTIALIAS)

    elif length != 0:
        ratio = (length / float(img.size[0]))
        height = int((float(img.size[1]) * float(ratio)))
        resized_img = img.resize((length, height), Image.ANTIALIAS)

    elif height != 0:
        ratio = (height / float(img.size[1]))
        length = int((float(img.size[0]) * float(ratio)))
        resized_img = img.resize((length, height), Image.ANTIALIAS)

    buffer = BytesIO()
    resized_img.save(fp=buffer, format=img_format)
    buff_val = buffer.getvalue()
    return ContentFile(buff_val)
