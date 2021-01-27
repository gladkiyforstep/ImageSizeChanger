from urllib.error import URLError
from django.core.files.uploadedfile import InMemoryUploadedFile
from compressor.models import Image, ChangedImage
from compressor.forms import SimpleAddImageForm, ChangeImageForm
from compressor.SizeChanger import size_changer
from imageio import imread


class ImageUploadHelper:

    def __init__(self, request):
        self.request = request
        self.form = SimpleAddImageForm(request.POST, request.FILES)

    def form_validator(self):
        if self.form.is_valid():
            return ''
        else:
            return "Ресурс с данной ссылкой не отвечет. Или загружаемый файл повреждён "

    def info_checker(self):
        is_file = 'photo' in self.request.FILES
        link = self.request.POST['link']
        if is_file and link != '':
            return "Удалите файл или ссылку"
        elif not is_file and link == '':
            return "Добавьте файл или ссылку"
        elif is_file:
            return 'file'
        elif link != '':
            return 'link'

    def object_creator(self):
        img_obj = Image.objects.filter(pk=1)
        link = self.request.POST['link']
        error = self.form_validator()
        if error != '':
            return {'error': error, 'obj': None, 'form': self.form}
        info = self.info_checker()
        if info == 'file':
            self.form.photo = self.request.FILES['photo']
            self.form.save(commit=True)
            img_obj = self.form.instance
        elif info == 'link':
            try:
                imread_file = imread(link)
                img_obj = Image(link=link)
                img_obj.get_remote_image()
            except URLError:
                error = "Не верная ссылка"
            except ValueError:
                error = "Нужна прямая ссылка на избражение"
        else:
            return {'error': info, 'obj': None, 'form': self.form}

        return {'error': error, 'obj': img_obj, 'form': self.form} if error == '' else {
            'error': error,
            'obj': None,
            'form': self.form
        }


class ChangingPageHelper:

    def __init__(self, request, original_obj):
        self.request = request
        self.form = ChangeImageForm(request.POST, request.FILES)
        self.original_image_obj = original_obj
        self.height = request.POST['height']
        self.length = request.POST['length']

    def form_validator(self):
        if self.form.is_valid():
            return ''
        else:
            return "Некорректные данные"

    def info_checker(self):
        if self.height == '':
            self.height = 0
        else:
            self.height = int(self.height)
        if self.length == '':
            self.length = 0
        else:
            self.length = int(self.length)
        if self.height == 0 and self.length == 0:
            return "Введите ширину и/или высоту"
        else:
            return ''

    @staticmethod
    def image_name_taker(obj):
        name = obj.photo.name
        name = name[name.rfind('/') + 1:]
        return name

    def object_creator(self):
        changed_image_obj = self.original_image_obj
        info_error = self.info_checker()
        if info_error != '':
            return {'form': self.form, 'error': info_error, 'obj': self.original_image_obj}
        form_error = self.form_validator()
        if form_error != '':
            return {'form': self.form, 'error': form_error, 'obj': self.original_image_obj}
        val_error = ''
        try:
            changed_image = size_changer(self.original_image_obj.photo, self.height, self.length)
            changed_image_file = InMemoryUploadedFile(
                changed_image,
                None,
                'resized.jpg',
                'image/jpeg',
                changed_image.tell,
                None
            )
            changed_image_obj = ChangedImage(
                height=self.height,
                length=self.length,
                photo=changed_image_file,
                not_changed_img=self.original_image_obj
            )
            changed_image_obj.save()
            changed_image_file.flush()

        except ValueError:
            val_error = 'Высота и Ширина должны быть целыми числами больше нуля.'
        if val_error != '':
            return {'form': self.form, 'error': val_error, 'obj': self.original_image_obj}
        else:
            return {'form': self.form, 'error': '', 'obj': changed_image_obj}

