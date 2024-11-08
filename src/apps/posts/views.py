from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from .models import Post
from apps.gallery.models import TemporaryImage, Image
from apps.gallery.utils import save_images

from friendship.models import Friend, Block


# Create your views here.

User = get_user_model()


@login_required
def post_detail_view(request, post_id, site_url):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.user and \
            (not post.is_visible or (not post.is_public and not Friend.objects.are_friends(request.user, post.user)) or
            Block.objects.is_blocked(request.user, post.user)):
        return render(request, 'core/access_denied.html')

    if 'post_previous_url' not in request.session:
        request.session['post_previous_url'] = request.META.get('HTTP_REFERER', '/')

    context = {
        'post': post,
        'is_post_detail': True,
        'go_back_button_url': request.session['post_previous_url']
    }
    return render(request, 'posts/post_detail_view.html', context)


@login_required
def post_create(request, site_url):
    user = get_object_or_404(User, site_url=site_url)
    if request.user != user:
        return redirect('posts:post_create', request.user.site_url)
    temporary_images = TemporaryImage.objects.filter(user=request.user)

    context = {
        'user': user,
        'temporary_images': temporary_images,
    }

    if 'new_post_description' in request.session:
        context['post_text_data'] = request.session.pop('new_post_description')

    if 'post_previous_url' not in request.session:
        request.session['post_previous_url'] = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        context['post_form'] = post_form

        if request.POST.get('add_post'):
            if post_form.is_valid():
                if not temporary_images and not post_form.cleaned_data['text']:
                    messages.error(request, "New post must have at least description or images.")
                    return render(request, 'posts/post_create_edit_form.html', context)

                else:
                    post = post_form.save(commit=False)
                    post.user = user
                    post.is_public = bool(int(request.POST.get('is_public')))
                    post.save()
                    save_images(request, post, temporary_images)

                    temporary_images.delete()
                    previous_url = request.session.pop('post_previous_url', '/')

                    return redirect(previous_url)

        elif request.POST.get('cancel'):
            temporary_images.delete()
            previous_url = request.session.pop('post_previous_url', '/')

            return redirect(previous_url)

    else:
        post_form = PostForm()
        context['post_form'] = post_form

    return render(request, 'posts/post_create_edit_form.html', context)


@login_required
def post_edit(request, site_url, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.user:
        return render(request, 'core/access_denied.html')

    post_images = Image.objects.filter(user=request.user, post=post)
    temporary_images = TemporaryImage.objects.filter(user=request.user)
    number_of_images_after_save = temporary_images.count() + len(
        [image for image in post_images if not image.edit_to_delete]
    )
    if 'post_edit_previous_url' not in request.session:
        request.session['post_edit_previous_url'] = request.META.get('HTTP_REFERER', '/')

    context = {
        'post': post,
        'temporary_images': temporary_images,
        'post_images': post_images,
        'number_of_images_after_save': number_of_images_after_save,
    }

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        context['post_form'] = post_form

        if request.POST.get('add_post'):
            if post_form.is_valid():
                if not number_of_images_after_save and not post_form.cleaned_data['text']:
                    messages.error(request, "New post must have at least description or images.")
                    return render(request, 'posts/post_create_edit_form.html', context)

                else:
                    if not number_of_images_after_save and not post.text:
                        post.is_visible = False
                    elif not post.is_visible:
                        post.is_visible = True

                    post.is_public = bool(int(request.POST.get('is_public')))
                    post = post_form.save()

                    save_images(request, post, temporary_images)

                    for image in post_images:
                        if image.edit_to_delete:
                            image.delete()
                    previous_url = request.session.pop('post_edit_previous_url')

                    return redirect(previous_url)

        elif request.POST.get('cancel'):
            temporary_images.delete()
            for image in post_images:
                if image.edit_to_delete:
                    image.edit_to_delete = False
                    image.save()
            previous_url = request.session.pop('post_edit_previous_url')

            return redirect(previous_url)
    else:
        post_form = PostForm(instance=post)
        context['post_form'] = post_form

    return render(request, 'posts/post_create_edit_form.html', context)


@login_required
def post_delete(request, site_url, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.user:
        return render(request, 'core/access_denied.html')

    post_images = Image.objects.filter(user=request.user, post=post)

    if 'post_previous_url' in request.session:
        request.session['post_delete_previous_url'] = request.session['post_previous_url']
    elif 'post_delete_previous_url' not in request.session:
        request.session['post_delete_previous_url'] = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        previous_url = request.session.pop('post_delete_previous_url')
        post.delete()

        return redirect(previous_url)

    context = {
        'post': post,
        'post_images': post_images,
        'previous_url': request.META.get('HTTP_REFERER', '/'),
    }

    return render(request, 'posts/post_delete_view.html', context)
