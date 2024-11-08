from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from friendship.models import Friend, Block, FriendshipRequest
from friendship.exceptions import AlreadyExistsError

from .utils import (remove_blocked_users, remove_blocked_users_from_requests, remove_friend_users,
                    unrejected_request_count_without_blocked_users, custom_user_list_serializer)

User = get_user_model()


@login_required
def friends_all_view(request):
    user_friends = Friend.objects.friends(request.user)
    user_friends = remove_blocked_users(request.user, user_friends)
    user_friends = sorted(user_friends, key=lambda item: item.first_name)
    user_friends_json = custom_user_list_serializer(user_friends)

    received_requests = Friend.objects.unrejected_requests(user=request.user)
    awaiting_requests_count = len(remove_blocked_users_from_requests(request.user, received_requests))

    context = {
        'is_all_section': True,
        'user_friends': user_friends,
        'user_friends_json': user_friends_json,
        'awaiting_requests_count': awaiting_requests_count,
    }

    return render(request, 'friends/friends_all.html', context)


@login_required
def friends_requests_received_view(request):
    received_requests = Friend.objects.unrejected_requests(user=request.user)
    friends_requests = remove_blocked_users_from_requests(request.user, received_requests, request_type='received')
    awaiting_requests_count = len(friends_requests)

    context = {
        'is_request_section': True,
        'is_received_section': True,
        'friends_requests': friends_requests,
        'awaiting_requests_count': awaiting_requests_count,
    }
    for friend_request in friends_requests:
        if not friend_request.viewed:
            friend_request.mark_viewed()

    return render(request, 'friends/friends_requests_received.html', context)


@login_required
def friends_requests_rejected_view(request):
    requests_rejected = Friend.objects.rejected_requests(user=request.user)
    friends_requests = remove_blocked_users_from_requests(request.user, requests_rejected, request_type='rejected')

    awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)

    context = {
        'is_request_section': True,
        'is_rejected_section': True,
        'friends_requests': friends_requests,
        'awaiting_requests_count': awaiting_requests_count,
    }

    return render(request, 'friends/friends_requests_rejected.html', context)


@login_required
def friends_requests_sent_view(request):
    requests_sent = Friend.objects.sent_requests(user=request.user)
    friends_requests = remove_blocked_users_from_requests(request.user, requests_sent, request_type='sent')
    awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)

    context = {
        'is_request_section': True,
        'is_sent_section': True,
        'friends_requests': friends_requests,
        'awaiting_requests_count': awaiting_requests_count,
    }

    return render(request, 'friends/friends_requests_sent.html', context)


@login_required
def blocked_users_view(request):
    blocked_users = Block.objects.blocking(request.user)
    awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)

    context = {
        'is_blocked_section': True,
        'blocked_users': blocked_users,
        'awaiting_requests_count': awaiting_requests_count,
    }

    return render(request, 'friends/blocked_users_view.html', context)


def friends_search_view(request):
    awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)

    all_users = User.objects.all().exclude(id=request.user.id).order_by('-id')[:100]
    all_users_no_friends = remove_friend_users(request.user, all_users)
    all_users_no_friends_no_block = remove_blocked_users(request.user, all_users_no_friends)
    all_users_no_friends_no_block.sort(key=lambda x: x.id, reverse=True)
    all_users = all_users_no_friends_no_block[:10]

    all_users_info = list()
    for item in all_users:
        try:
            FriendshipRequest.objects.get(from_user=request.user, to_user=item)
            request_info = 'sent'
        except:
            try:
                FriendshipRequest.objects.get(from_user=item, to_user=request.user)
                request_info = 'received'
            except:
                request_info = None
        all_users_info.append({'user': item, 'request_info': request_info})

    context = {
        'all_users': all_users,
        'all_users_info': all_users_info,
        'is_friends_search_section': True,
        'awaiting_requests_count': awaiting_requests_count,
    }

    return render(request, 'friends/friends_friend_search.html', context)


# AJAX views
def friends_search_result(request):
    """ Friends search results data """
    if request.method == "POST":
        user_data = request.POST.get('userData')
        matching_users_list = User.objects.filter(Q(first_name__icontains=user_data) | Q(last_name__icontains=user_data))
        matching_users_list_no_block = remove_blocked_users(request.user, matching_users_list)
        matching_users_list_no_block_no_friends = remove_friend_users(request.user, matching_users_list_no_block)[:20]

        if len(matching_users_list_no_block_no_friends) > 0 and len(user_data) > 0:
            found_users = []
            for user in matching_users_list_no_block_no_friends:
                item = {
                    'pk': user.pk,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'site_url': user.site_url,
                    'gender': user.data.gender,
                }

                try:
                    request_sent = FriendshipRequest.objects.get(from_user=request.user, to_user=user)
                    item['request_info'] = 'sent'
                except:
                    try:
                        request_received = FriendshipRequest.objects.get(from_user=user, to_user=request.user)
                        item['request_info'] = 'received'
                    except:
                        item['request_info'] = 'none'

                if user.data.profile_image:
                    item['profile_image_url'] = user.data.profile_image.image.url
                else:
                    item['profile_image_url'] = None
                found_users.append(item)
        else:
            found_users = 'There is no matching user'
        return JsonResponse({'foundUsers': found_users})
    return JsonResponse({})


@login_required
def check_friendship_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        are_friends = Friend.objects.are_friends(request.user, user)
        return JsonResponse({'are_friends': are_friends})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)


@login_required
def send_friend_request(request, user_id):
    """ Send friendship request """
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
            Friend.objects.add_friend(request.user, to_user=user)
            return JsonResponse({'success': True})
        except AlreadyExistsError:
            return JsonResponse({'success': False, 'error': 'Friendship request already exists'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def friends_request_accept(request, friendship_request_id):
    """ Accept friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.accept()
        awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)
        response = {
            'success': True,
            'awaiting_requests_count': awaiting_requests_count,
        }
        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def friends_request_reject(request, friendship_request_id):
    """ Reject friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.reject()
        awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)
        response = {
            'success': True,
            'awaiting_requests_count': awaiting_requests_count,
        }
        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def friends_request_cancel(request, friendship_request_id):
    """ Cancel friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.cancel()
        requests_sent = Friend.objects.sent_requests(user=request.user)
        friends_requests = remove_blocked_users_from_requests(request.user, requests_sent, request_type='sent')
        sent_requests_count = len(friends_requests)
        response = {
            'success': True,
            'sent_requests_count': sent_requests_count,
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def blocked_add_block(request, user_id, request_type):
    """Block user"""
    if request.method == "POST":
        try:
            blocked = User.objects.get(id=user_id)
            blocker = request.user
            Block.objects.add_block(blocker, blocked)

            awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)
            response = {
                'success': True,
                'awaiting_requests_count': awaiting_requests_count,
            }

            if request_type == 'all':
                user_friends = Friend.objects.friends(request.user)
                user_friends = remove_blocked_users(request.user, user_friends)
                response['friends_count'] = len(user_friends)
            elif request_type == 'received':
                response['requests_count'] = response['awaiting_requests_count']
            elif request_type == 'rejected':
                requests_rejected = Friend.objects.rejected_requests(user=request.user)
                friends_requests = remove_blocked_users_from_requests(request.user, requests_rejected, request_type)
                response['requests_count'] = len(friends_requests)
            elif request_type == 'sent':
                requests_sent = Friend.objects.sent_requests(user=request.user)
                friends_requests = remove_blocked_users_from_requests(request.user, requests_sent, request_type)
                response['requests_count'] = len(friends_requests)

            return JsonResponse(response, status=200)
        except AlreadyExistsError as e:
            return JsonResponse({'success': False, 'error': 'User is already blocked'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def blocked_remove_block(request, user_id):
    """Unblock user"""
    if request.method == "POST":
        try:
            blocked = User.objects.get(id=user_id)
            blocker = request.user
            Block.objects.remove_block(blocker, blocked)

            blocked_users_count = len(Block.objects.blocking(request.user))
            awaiting_requests_count = unrejected_request_count_without_blocked_users(request.user)
            response = {
                'success': True,
                'blocked_users_count': blocked_users_count,
                'awaiting_requests_count': awaiting_requests_count,
            }
            return JsonResponse(response, status=200)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def friends_remove_friend(request, friend_id):
    """Remove user from friends"""
    if request.method == "POST":
        try:
            friend = User.objects.get(id=friend_id)
            Friend.objects.remove_friend(request.user, friend)

            user_friends = Friend.objects.friends(request.user)
            user_friends = remove_blocked_users(request.user, user_friends)
            response = {
                'success': True,
                'friends_count': len(user_friends),
            }
            return JsonResponse(response, status=200)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
