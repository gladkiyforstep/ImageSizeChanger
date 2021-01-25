from urllib.error import URLError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from compressor.models import Image, ChangedImage
from compressor.forms import SimpleAddImageForm, ChangeImageForm
from compressor.SizeChanger import size_changer
from imageio import imread


def image_upload_view(request):
    home_url = request.get_full_path()
    home_url = home_url[:home_url.rfind('upload')] + 'home/'
    error = False
    img_obj = get_object_or_404(Image, pk=1)
    if request.method == 'POST':
        form = SimpleAddImageForm(request.POST, request.FILES)
        if form.is_valid():
            if 'photo' in request.FILES:
                if request.POST['link'] == '':
                    form.photo = request.FILES['photo']
                    form.save(commit=True)
                    img_obj = form.instance
                else:
                    error = "Удалите файл или ссылку"

            else:
                if request.POST['link'] == '':
                    error = "Добавьте файл или ссылку"

                else:
                    try:
                        link = request.POST['link']
                        imread_file = imread(link)
                        img_obj = Image(link=link)
                        img_obj.get_remote_image()
                    except URLError:
                        error = "Не верная ссылка"
                    except ValueError:
                        error = "Нужна прямая ссылка на избражение"
        else:
            error = 'Ресурс с данной ссылкой не отвечет. Или загружаемый файл повреждён '

        if error:
            return render(request, 'index.html', {'form': form, 'home_url': home_url, 'error': error})
        else:
            return redirect('/changing_page/'+str(img_obj.pk))
    else:
        form = SimpleAddImageForm()
        return render(request, 'index.html', {'form': form, 'home_url': home_url})


def home_page_view(request):
    upload_url = request.get_full_path()
    upload_url = upload_url[:upload_url.rfind('home')] + 'upload/'
    images = Image.objects.all()
    all_images = []
    for img in images:
        if img.photo:
            img_info = {
                'title': img.photo.name[img.photo.name.rfind('/')+1:],
                'photo': img.photo.url[:img.photo.url.rfind('media')]+'changing_page/'+str(img.id)
            }
            all_images.append(img_info)
    context = {'all_images': all_images, 'upload_url': upload_url}

    return render(request, 'home.html', context)


def changing_page_view(request, pk):
    home_url = request.get_full_path()
    home_url = home_url[:home_url.rfind('changing_page')] + 'home/'
    error = False
    original_image_obj = get_object_or_404(Image, pk=pk)
    original_image_name = original_image_obj.photo.name
    original_image_name = original_image_name[original_image_name.rfind('/') + 1:]
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
            try:
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
                changed_image_name = changed_image_obj.photo.name
                changed_image_name = changed_image_name[changed_image_name.rfind('/') + 1:]
            except ValueError:
                error = 'Высота и Ширина должны быть целыми числами больше нуля.'
            if error:
                return render(request, 'changing.html',
                              {
                                  'form': form,
                                  'img_obj': original_image_obj,
                                  'name': original_image_name,
                                  'home_url': home_url,
                                  'error': error
                              })
            else:
                return render(request, 'changing.html',
                              {
                                  'form': form,
                                  'img_obj': changed_image_obj,
                                  'name': changed_image_name,
                                  'home_url': home_url
                              })

    else:
        form = ChangeImageForm(instance=original_image_obj)

        return render(request, 'changing.html',
                      {
                          'form': form,
                          'img_obj': original_image_obj,
                          'name': original_image_name,
                          'home_url': home_url
                      })



