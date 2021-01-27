from django.shortcuts import render, redirect, get_object_or_404
from compressor.models import Image, ChangedImage
from compressor.forms import SimpleAddImageForm, ChangeImageForm
from compressor.ViewsHelper import ImageUploadHelper, ChangingPageHelper



def image_upload_view(request):
    home_url = '/home/'
    if request.method == 'POST':
        helper = ImageUploadHelper(request)
        created_obj = helper.object_creator()
        error = created_obj['error']
        img_obj = created_obj['obj']
        form = created_obj['form']
        if error != '':
            return render(request, 'index.html', {'form': form, 'home_url': home_url, 'error': error})
        else:
            return redirect('/changing_page/'+str(img_obj.pk))
    else:
        form = SimpleAddImageForm()
        return render(request, 'index.html', {'form': form, 'home_url': home_url})


def home_page_view(request):
    upload_url = '/upload/'
    if not Image.objects.filter(pk=1).exists():
        message = "Нет доступных изображений"
        return render(request, 'home.html', {'message': message, 'upload_url': upload_url})
    images = Image.objects.all()
    all_images = []
    for img in images:
        if img.photo:
            img_info = {
                'title': img.photo.name[img.photo.name.rfind('/')+1:],
                'photo': img.photo.url[:img.photo.url.rfind('media')]+'changing_page/'+str(img.id)
            }
            all_images.append(img_info)


    return render(request, 'home.html', {'all_images': all_images, 'upload_url': upload_url})


def changing_page_view(request, pk):
    home_url = '/home/'
    original_image_obj = get_object_or_404(Image, pk=pk)
    original_image_name = ChangingPageHelper.image_name_taker(original_image_obj)

    if request.method == 'POST':
        helper = ChangingPageHelper(request, original_image_obj)
        created_obj = helper.object_creator()
        form = created_obj['form']
        error = created_obj['error']
        changed_image_obj = created_obj['obj']
        changed_image_name = ChangingPageHelper.image_name_taker(changed_image_obj)

        # if form.is_valid():
        #     try:
        #         changed_image = size_changer(original_image_obj.photo, height, length)
        #         changed_image_file = InMemoryUploadedFile(
        #             changed_image,
        #             None,
        #             'resized.jpg',
        #             'image/jpeg',
        #             changed_image.tell,
        #             None
        #         )
        #         changed_image_obj = ChangedImage(
        #             height=height,
        #             length=length,
        #             photo=changed_image_file,
        #             not_changed_img=original_image_obj
        #         )
        #         changed_image_obj.save()
        #         changed_image_name = changed_image_obj.photo.name
        #         changed_image_name = changed_image_name[changed_image_name.rfind('/') + 1:]
        #     except ValueError:
        #         error = 'Высота и Ширина должны быть целыми числами больше нуля.'
        if error != '':
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
