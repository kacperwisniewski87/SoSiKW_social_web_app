from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Count

from apps.posts.models import Post
from apps.gallery.models import Image, TemporaryImage, Album
from apps.gallery.utils import add_gallery_section
from apps.users.forms import UserProfileChangeForm
from apps.friends.utils import (remove_blocked_users, unrejected_request_count_without_blocked_users,
                                remove_blocked_users_from_requests, custom_user_list_serializer)
from apps.chat.models import ChatRoom
from apps.common import utils as cleanups

from friendship.models import Friend, FriendshipRequest, Block


# Create your views here.
User = get_user_model()


def friendship_status(from_user, to_user, context):
    is_friend = Friend.objects.are_friends(from_user, to_user)
    context['is_friend'] = is_friend
    context['request_sent'] = bool(len(FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user)))
    context['request_received'] = bool(len(FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user)))

    chat_room = ChatRoom.objects.filter(
        is_group=False,
        users__in=[from_user, to_user]
    ).annotate(
        num_users=Count('users')
    ).filter(
        num_users=2
    ).distinct()
    context['chat_room'] = chat_room[0] if chat_room else None


def add_post_section(context):
    context['is_post_section'] = True


def add_info_section(context):
    context['is_info_section'] = True


def add_friends_section(context):
    context['is_friends_section'] = True


@login_required
def profile_main_view(request, site_url):
    cleanups.previous_url_cleanup(request)

    user = get_object_or_404(User, site_url=site_url)

    if Block.objects.is_blocked(request.user, user):
        return render(request, 'core/access_denied.html')

    if user == request.user or Friend.objects.are_friends(request.user, user):
        posts = Post.objects.filter(user=user, is_visible=True)
    else:
        posts = Post.objects.filter(user=user, is_visible=True, is_public=True)
    images = Image.objects.filter(user=user, post__in=posts)[:9]

    if request.method == 'POST':
        cleanups.temporary_data_cleanup(request.user)
        temp_images = request.FILES.getlist('images')
        request.session['new_post_description'] = request.POST.get('new_post_description')

        for image in temp_images:
            TemporaryImage.objects.create(
                image=image,
                user=request.user,
            )

        return redirect('posts:post_create', site_url=request.user.site_url)

    context = {
        'user': user,
        'posts': posts,
        'images': images,
    }

    if user != request.user:
        friendship_status(request.user, user, context)
    add_post_section(context)

    return render(request, 'account/profile_posts_view.html', context)


@login_required
def profile_info_view(request, site_url):
    cleanups.previous_url_cleanup(request)

    user = get_object_or_404(User, site_url=site_url)

    if Block.objects.is_blocked(request.user, user):
        return render(request, 'core/access_denied.html')

    context = {
        'user': user,
    }

    if user != request.user:
        friendship_status(request.user, user, context)
    add_info_section(context)

    return render(request, 'account/profile_info_view.html', context)


@login_required
def profile_info_edit_view(request, site_url):
    user = get_object_or_404(User, site_url=site_url)
    if request.user != user:
        return render(request, 'core/access_denied.html')

    if request.method == 'POST':
        form = UserProfileChangeForm(request.POST, instance=user.data)

        if form.is_valid():
            form.save()

            return redirect('account:profile_info_view', user.site_url)

    else:
        form = UserProfileChangeForm()
    context = {
        'user': user,
        'form': form,
    }

    add_info_section(context)

    return render(request, 'account/profile_info_edit_view.html', context)


@login_required
def friends_main_view(request, site_url):
    cleanups.previous_url_cleanup(request)

    user = get_object_or_404(User, site_url=site_url)

    if Block.objects.is_blocked(request.user, user):
        return render(request, 'core/access_denied.html')

    user_friends = Friend.objects.friends(user)
    user_friends = remove_blocked_users(user, user_friends)
    user_friends = sorted(user_friends, key=lambda item: item.first_name)
    user_friends_json = custom_user_list_serializer(user_friends)
    awaiting_friends_requests = unrejected_request_count_without_blocked_users(user=request.user)

    context = {
        'user': user,
        'user_friends': user_friends,
        'user_friends_json': user_friends_json,
        'is_all_section': True,
        'awaiting_friends_requests': awaiting_friends_requests,
    }

    if user != request.user:
        friendship_status(request.user, user, context)
    add_friends_section(context)

    return render(request, 'account/profile_friends_view.html', context)


@login_required
def user_all_photos_view(request, site_url):
    cleanups.previous_url_cleanup(request)

    user = get_object_or_404(User, site_url=site_url)

    if Block.objects.is_blocked(request.user, user):
        return render(request, 'core/access_denied.html')

    if request.user == user or Friend.objects.are_friends(request.user, user):
        posts = Post.objects.filter(user=user, is_visible=True)
    else:
        posts = Post.objects.filter(user=user, is_visible=True, is_public=True)
    images = Image.objects.filter(user=user, post__in=posts)

    if request.method == "POST":
        cleanups.temporary_data_cleanup(request.user)
        temp_images = request.FILES.getlist('images')

        for image in temp_images:
            TemporaryImage.objects.create(
                image=image,
                user=request.user,
            )

        return redirect('posts:post_create', site_url=request.user.site_url)

    context = {
        'user': user,
        'images': images,
        'albums_page': False,
    }

    if user != request.user:
        friendship_status(request.user, user, context)
    add_gallery_section(context)

    return render(request, 'account/profile_gallery_photos_view.html', context)


@login_required
def user_albums_view(request, site_url):
    cleanups.previous_url_cleanup(request)

    user = get_object_or_404(User, site_url=site_url)

    if Block.objects.is_blocked(request.user, user):
        return render(request, 'core/access_denied.html')

    if user == request.user:
        albums = Album.objects.filter(user=user)
    else:
        all_albums = Album.objects.filter(user=user, is_private=False)

        if Friend.objects.are_friends(request.user, user):
            albums = [album for album in all_albums if album.post.is_visible]
        else:
            albums = [album for album in all_albums if (album.post.is_visible and album.post.is_public)]

    if request.method == "POST":
        cleanups.temporary_data_cleanup(request.user)
        temp_images = request.FILES.getlist('images')

        for image in temp_images:
            TemporaryImage.objects.create(
                image=image,
                user=request.user,
            )

        return redirect('posts:post_create', site_url=request.user.site_url)

    context = {
        'user': user,
        'albums': albums,
        'albums_page': True,
    }

    if user != request.user:
        friendship_status(request.user, user, context)
    add_gallery_section(context)

    return render(request, 'account/profile_gallery_albums_view.html', context)


def hud_open_get_user_data(request, site_url):
    if request.method == "GET":
        user = get_object_or_404(User, site_url=site_url)

        if user.data.profile_image:
            profile_picture_url = user.data.profile_image.image.url
        else:
            if user.data.gender == 'male':
                profile_picture_url = '/static/images/gallery_icons/avatar-male.png'
            elif user.data.gender == 'female':
                profile_picture_url = '/static/images/gallery_icons/avatar-female.png'
            else:
                profile_picture_url = '/static/images/gallery_icons/avatar-default.png'

        response = {
            'success': True,
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture_url': profile_picture_url,
        }
        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
