from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.posts.models import Post
from apps.gallery.models import TemporaryImage
from apps.friends.utils import unrejected_request_count_without_blocked_users, remove_blocked_users
from apps.common import utils as cleanups

from friendship.models import Friend


# Create your views here.

User = get_user_model()


@login_required
def main_view(request):
    friends = Friend.objects.friends(request.user)
    friends = remove_blocked_users(request.user, friends)
    friends.append(request.user)

    posts = Post.objects.filter(user__in=friends, is_visible=True, is_public=True)
    awaiting_friends_requests = unrejected_request_count_without_blocked_users(user=request.user)

    cleanups.previous_url_cleanup(request)

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
        'posts': posts,
        'awaiting_friends_requests': awaiting_friends_requests,
    }

    return render(request, 'core/index.html', context)
