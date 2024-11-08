from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from apps.posts.forms import PostForm
from apps.posts.models import Post

from .forms import AlbumForm
from .models import Image, Album, TemporaryImage
from .utils import add_gallery_section, save_images

from friendship.models import Friend, Block

# Create your views here.
User = get_user_model()


# view functions


def image_preview(request, image_id, post_type, post_id):
    image = get_object_or_404(Image, id=image_id)
    user = image.user

    if (not image.post.is_visible or (not image.post.is_public and not Friend.objects.are_friends(request.user, user))
            or Block.objects.is_blocked(request.user, user)):
        return render(request, 'core/access_denied.html')

    post_images_count = image.post.images.count()

    if post_images_count > 1 or (post_images_count == 1 and image.description):
        image_description = image.description
    else:
        image_description = image.post.text

    if 'image_previous_url' not in request.session:
        request.session['image_previous_url'] = request.META.get('HTTP_REFERER', '/')

    context = {
        'image': image,
        'post_type': post_type,
        'exit_url': request.session['image_previous_url'],
        'image_description': image_description,
    }

    if post_type == 'p':
        post = get_object_or_404(Post, id=post_id)
        images = post.images.all()

    elif post_type == 'a':
        images = Image.objects.filter(user=user)

    next_images = images.filter(Q(created_at__lt=image.created_at) | Q(created_at=image.created_at, id__lt=image.id))
    if next_images:
        next_image = next_images.order_by("-created_at", "id")[0]
        context['next_image'] = next_image

    prev_images = images.filter(Q(created_at__gt=image.created_at) | Q(created_at=image.created_at, id__gt=image.id))
    if prev_images:
        prev_image = prev_images.order_by("created_at", "id")[0]
        context['prev_image'] = prev_image

    return render(request, 'gallery/image_preview.html', context)


@login_required
def image_edit(request, image_id, post_type, post_id):
    image = get_object_or_404(Image, id=image_id)
    if request.user != image.user:
        return render(request, 'core/access_denied.html')

    post_images_count = image.post.images.count()

    if post_images_count > 1 or (post_images_count == 1 and image.description):
        image_description = image.description
    else:
        image_description = image.post.text

    if request.method == 'POST':
        if post_images_count > 1 or (post_images_count == 1 and image.description):
            image.description = request.POST.get('description')
            image.save()
        else:
            image.post.text = request.POST.get('description')
            image.post.save()

        return redirect('gallery:image_preview', image_id=image.id, post_type=post_type, post_id=post_id)

    context = {
        'image': image,
        'image_description': image_description,
        'post_type': post_type,
    }

    return render(request, 'gallery/image_edit.html', context)


@login_required
def image_delete(request, image_id, post_type, post_id):
    image = get_object_or_404(Image, id=image_id)
    if request.user != image.user:
        return render(request, 'core/access_denied.html')

    post_images_count = image.post.images.count()
    is_album_image = Album.objects.filter(post=image.post)

    if request.method == 'POST':
        if post_images_count > 1:
            image.delete()
        elif is_album_image:
            image.post.is_visible = False
            image.post.save()
            image.delete()
        else:
            image.post.delete()

        if 'image_previous_url' not in request.session:
            return redirect(request.session['image_previous_url'])
        else:
            return redirect('core:main')

    context = {
        'image': image,
        'post_type': post_type,
        'post_images_count': post_images_count,
        'is_album_image': is_album_image,
    }

    return render(request, 'gallery/image_delete.html', context)


@login_required
def album_preview(request, uuid_url):
    album = get_object_or_404(Album, uuid_url=uuid_url)
    if (request.user != album.user and (not album.post.is_visible or
            (not album.post.is_public and not Friend.objects.are_friends(request.user, album.user))) or
            Block.objects.is_blocked(request.user, album.user)):
        return render(request, 'core/access_denied.html')

    images = Image.objects.filter(post=album.post)

    if 'album_previous_url' not in request.session:
        request.session['album_previous_url'] = request.META.get('HTTP_REFERER', '/')

    context = {
        'user': album.user,
        'album': album,
        'album_images': images,
        'albums_page': True,
    }
    add_gallery_section(context)

    return render(request, 'gallery/album_preview.html', context)


@login_required
def album_create(request):
    temporary_images = TemporaryImage.objects.filter(user=request.user)
    number_of_images_after_save = temporary_images.count()

    if request.method == 'POST':
        updated_request = request.POST.copy()
        if not request.POST.get('title'):
            updated_request.update({'title': 'No name album'})

        album_form = AlbumForm(updated_request)
        post_form = PostForm(updated_request)

        if request.POST.get('create_album'):
            if album_form.is_valid() and post_form.is_valid():
                post = post_form.save(commit=False)
                album = album_form.save(commit=False)
                post.user = request.user
                post.is_public = bool(int(request.POST.get('is_public')))
                if not album.is_private and number_of_images_after_save:
                    post.is_visible = True
                else:
                    post.is_visible = False
                post.save()

                album.user = request.user
                album.post = post
                album.save()

                save_images(request, post, temporary_images)

                return redirect('gallery:album_preview', album.uuid_url)

        elif request.POST.get('cancel'):
            temporary_images.delete()

            return redirect('account:user_albums_view', request.user.site_url)
    else:
        album_form = AlbumForm()
        post_form = PostForm()
    context = {
        'album_form': album_form,
        'post_form': post_form,
        'temporary_images': temporary_images,
        'number_of_images_after_save': number_of_images_after_save,
    }
    return render(request, 'gallery/album_create_edit.html', context)


@login_required
def album_edit(request, uuid_url):
    album = get_object_or_404(Album, uuid_url=uuid_url)
    if request.user != album.user:
        return render(request, 'core/access_denied.html')

    album_images = Image.objects.filter(user=request.user, post=album.post)
    temporary_images = TemporaryImage.objects.filter(user=request.user)
    number_of_images_after_save = temporary_images.count() + len(
        [image for image in album_images if not image.edit_to_delete]
    )

    if 'post_edit_previous_url' not in request.session:
        request.session['post_edit_previous_url'] = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        updated_request = request.POST.copy()
        if not request.POST.get('title'):
            updated_request.update({'title': album.title})

        album_form = AlbumForm(updated_request, instance=album)
        post_form = PostForm(updated_request, instance=album.post)
        previous_url = request.session.pop('post_edit_previous_url')

        if request.POST.get('create_album'):
            if album_form.is_valid() and post_form.is_valid():
                post = post_form.save(commit=False)
                album = album_form.save(commit=False)

                if not album.is_private and number_of_images_after_save:
                    post.is_visible = True
                else:
                    post.is_visible = False

                post.is_public = bool(int(request.POST.get('is_public')))
                post.save()
                album.save()

                save_images(request, album.post, temporary_images)

                for image in album_images:
                    if image.edit_to_delete:
                        image.delete()
                    else:
                        field_name = 'album_img_description_' + str(image.id)
                        if (field_name in request.POST
                                and image.description != request.POST.get(field_name)):
                            image.description = request.POST.get(field_name)
                            image.save()

                return redirect(previous_url)

        elif request.POST.get('cancel'):
            temporary_images.delete()
            for image in album_images:
                if image.edit_to_delete:
                    image.edit_to_delete = False
                    image.save()

            return redirect(previous_url)
    else:
        album_form = AlbumForm(instance=album)
        post_form = PostForm(instance=album.post)
    context = {
        'album_form': album_form,
        'album': album,
        'post_form': post_form,
        'post': album.post,
        'temporary_images': temporary_images,
        'album_images': album_images,
    }
    return render(request, 'gallery/album_create_edit.html', context)


@login_required
def album_delete(request, uuid_url):
    album = get_object_or_404(Album, uuid_url=uuid_url)
    if request.user != album.user:
        return render(request, 'core/access_denied.html')

    album_images = Image.objects.filter(user=request.user, post=album.post)

    if 'post_previous_url' in request.session:
        request.session['post_delete_previous_url'] = request.session['post_previous_url']
    elif 'album_previous_url' in request.session:
        request.session['post_delete_previous_url'] = request.session['album_previous_url']
    elif 'post_delete_previous_url' not in request.session:
        request.session['post_delete_previous_url'] = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        previous_url = request.session.pop('post_delete_previous_url')
        album.post.delete()

        return redirect(previous_url)

    context = {
        'album': album,
        'album_images': album_images,
        'post': album.post,
        'previous_url': request.META.get('HTTP_REFERER', '/'),
    }

    return render(request, 'gallery/album_delete.html', context)


@login_required
def toggle_image_delete_status(request, image_id, uuid_url=None, post_id=None, site_url=None):
    if request.method == 'POST':
        image = get_object_or_404(Image, id=image_id)
        if request.user != image.user:
            return render(request, 'core/access_denied.html')

        image.edit_to_delete = not image.edit_to_delete
        image.save()

        response_data = {
            'success': True,
            'edit_to_delete': image.edit_to_delete,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def upload_temp_images(request, site_url=None, uuid_url=None, post_id=None):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        post = None
        if uuid_url:
            album = get_object_or_404(Album, uuid_url=uuid_url)
            post = album.post

        response_data = []
        for image in images:
            temp_image = TemporaryImage.objects.create(
                image=image,
                user=request.user,
                post=post,
            )
            response_data.append({
                'success': True,
                'image_url': temp_image.image.url,
                'image_id': temp_image.id,
            })
        return JsonResponse(response_data, safe=False)
    return JsonResponse({'success': False}, status=400)


@login_required
def delete_temp_image(request, image_id, site_url=None, uuid_url=None, post_id=None):
    if request.method == 'POST':
        temp_image = TemporaryImage.objects.get(user=request.user, id=image_id)
        temp_image.delete()

        response_data = {
            'success': True,
            'message': 'Image deleted successfully',
        }

        return JsonResponse(response_data, status=200)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def delete_all_temp_images(request, site_url=None, uuid_url=None, post_id=None):
    if request.method == 'POST':
        temp_images = TemporaryImage.objects.filter(user=request.user)
        temp_images.delete()

        return JsonResponse({'message': 'Temporary images deleted'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)
