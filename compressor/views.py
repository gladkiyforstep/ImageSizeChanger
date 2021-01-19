from django.http import HttpResponse
from django.shortcuts import render
from compressor.models import Image
from compressor.forms import SimpleAddImageForm


def image_upload_view(request):
    form = SimpleAddImageForm()
    if request.method == 'POST':
        form = SimpleAddImageForm(request.POST, request.FILES)
        if form.is_valid():
            if 'photo' in request.FILES:
                form.photo = request.FILES['photo']
            form.save(commit=True)
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
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


