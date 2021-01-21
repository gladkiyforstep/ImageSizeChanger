import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from compressor.models import Image, ChangedImage
from compressor.forms import SimpleAddImageForm, ChangeImageForm
from compressor.SizeChanger import size_changer


def image_upload_view(request):
    form = SimpleAddImageForm()
    if request.method == 'POST':
        form = SimpleAddImageForm(request.POST, request.FILES)
        if form.is_valid():
            if 'photo' in request.FILES:
                form.photo = request.FILES['photo']
            form.save(commit=True)
            img_obj = form.instance
            return redirect('/changing_page/'+str(img_obj.pk))
    else:
        form = SimpleAddImageForm()
        return render(request, 'index.html', {'form': form})


def home(request):
    images = Image.objects.all()
    all_images = []
    for img in images:
        img_info = {
            'title': img.title,
            'photo': img.photo.url
        }
        all_images.append(img_info)
    context = {'all_images': all_images}

    return render(request, 'home.html', context)


def change(request, pk):
    original_image_obj = get_object_or_404(Image, pk=pk)

    if request.method == 'POST':
        height = 0
        length = 0
        form = ChangeImageForm(request.POST, request.FILES)
        if request.POST['height'] == '':
            height = 0
        else:
            height = int(request.POST['height'])
        if request.POST['length'] == '':
            length = 0
        else:
            length = int(request.POST['length'])
        if form.is_valid():
            changed_image = size_changer(original_image_obj.photo, height, length)
            changed_image_file = InMemoryUploadedFile(
                changed_image,
                None,
                'resized.jpg',
                'image/jpeg',
                changed_image.tell,
                None
            )
            changed_image_obj = ChangedImage(
                height=height,
                length=length,
                photo=changed_image_file,
                not_changed_img=original_image_obj
            )
            changed_image_obj.save()

            return render(request, 'changing.html', {'form': form, 'img_obj': changed_image_obj})

    else:
        form = ChangeImageForm(instance=original_image_obj)
        return render(request, 'changing.html', {'form': form, 'img_obj': original_image_obj})



