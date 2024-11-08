from apps.gallery.models import TemporaryImage


def temporary_data_cleanup(user, temporary_images=None):
    if not temporary_images:
        temporary_images = TemporaryImage.objects.filter(user=user)
    if temporary_images:
        for image in temporary_images:
            image.delete()


def previous_url_cleanup(request):
    if 'image_previous_url' in request.session:
        request.session.pop('image_previous_url')
    if 'album_previous_url' in request.session:
        request.session.pop('album_previous_url')
    if 'post_previous_url' in request.session:
        request.session.pop('post_previous_url')
    if 'post_delete_previous_url' in request.session:
        request.session.pop('post_delete_previous_url')
    if 'post_edit_previous_url' in request.session:
        request.session.pop('post_edit_previous_url')
