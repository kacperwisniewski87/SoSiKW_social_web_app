import os
from django.core.files.base import ContentFile

from apps.gallery.models import Album, Image, TemporaryImage


def add_gallery_section(context):
    context['is_gallery_section'] = True


def save_images(request, post, temporary_images):
    for temp_image in temporary_images:
        image = temp_image.image
        filecontent = ContentFile(image.file.read())
        filename = os.path.split(image.file.name)[-1]
        field_name = 'temp_img_description_' + str(temp_image.id)

        if request.POST and (field_name in request.POST):
            description = request.POST.get(field_name)
        else:
            description = ""

        new_image = Image.objects.create(
            user=request.user,
            post=post,
            description=description,
        )
        new_image.image.save(filename, filecontent)
        image.file.close()
        temp_image.delete()
