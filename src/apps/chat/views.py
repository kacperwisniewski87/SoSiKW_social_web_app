import json
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .models import ChatRoom, Message, LastVisitedRoom
from .utils import chat_rooms_navbar_data
from friendship.models import Friend
from apps.friends.utils import remove_blocked_users

User = get_user_model()


@login_required
def rooms_all(request):
    last_room = LastVisitedRoom.objects.get(user=request.user)
    if last_room.room:
        return redirect('chat:room_detail_view', last_room.room.uuid_url)
    else:
        chat_rooms = chat_rooms_navbar_data(request.user)

        context = {
            'chat_rooms': chat_rooms,
            'chat_rooms_json': json.dumps(chat_rooms),
        }

        return render(request, 'chat/no_chat_view.html', context)


@login_required
def room_detail(request, uuid_url):
    chat_room = get_object_or_404(ChatRoom, uuid_url=uuid_url)
    if request.user not in chat_room.users.all():
        return render(request, 'core/access_denied.html')

    messages = Message.objects.filter(room=chat_room)
    chat_users = chat_room.users.all()
    chat_users_count = len(chat_users)
    last_room = LastVisitedRoom.objects.get(user=request.user)
    last_room.set_visited_room(chat_room)

    chat_rooms = chat_rooms_navbar_data(request.user)

    read_by = chat_room.get_last_message_read_by()

    if messages and (request.user.id not in read_by):
        read_by.append(request.user.id)
        chat_room.set_last_message_read_by(read_by)
        chat_room.save()

    context = {
        'chat_room': chat_room,
        'messages': messages,
        'chat_rooms': chat_rooms,
        'chat_rooms_json': json.dumps(chat_rooms),
    }

    if chat_users_count == 2 and not chat_room.is_group:
        chat_with_user = chat_users[0] if chat_users[0] != request.user else chat_users[1]
        is_friend = Friend.objects.are_friends(request.user, chat_with_user)
        context['user_is_friend'] = is_friend
        context['chat_with_user'] = chat_with_user
    elif chat_users_count > 2 or (chat_users_count == 2 and chat_room.is_group):
        chat_users_data = list()
        for item in chat_users:
            if item == request.user:
                continue
            else:
                is_friend = Friend.objects.are_friends(request.user, item)
                chat_users_data.append({
                    'user': item,
                    'is_friend': is_friend,
                })
        context['chat_users_data'] = chat_users_data
    else:
        context['user_deleted'] = True

    return render(request, 'chat/chat_detail_view.html', context)


# AJAX views

def create_group_chat(request):
    if request.method == "POST":
        chat_name = request.POST.get('chat_name').strip()
        chat_name_length = len(chat_name)
        if 255 >= chat_name_length > 0:
            users_id_list_string = json.loads(request.POST.get('added_users_id'))
            users_id_list = [int(item) for item in users_id_list_string if item.isdecimal()]
            users_to_add = User.objects.filter(id__in=users_id_list)

            new_group_chat = ChatRoom.objects.create(
                name=chat_name,
                owner=request.user,
                is_group=True,
            )
            new_group_chat.users.add(*users_to_add, request.user)
            new_group_chat.save()

            response = {
                'success': True,
                'redirect_url': r"chat/" + new_group_chat.uuid_url,
            }

            return JsonResponse(response, status=200)

        elif chat_name_length > 255:
            response = {
                'success': False,
                'error_message': 'Too long',
            }
            return JsonResponse(response, status=200)

        else:
            return JsonResponse({'success': False, 'error': 'Chat name is empty'}, status=400)


def add_friends_to_group_chat(request, uuid_url):
    if request.method == "POST":
        try:
            chat_room = ChatRoom.objects.get(uuid_url=uuid_url)
        except:
            return JsonResponse({'success': False, 'error': 'Chat not found'}, status=400)
        if chat_room.is_group:
            users_id_list_string = json.loads(request.POST.get('added_users_id'))
            users_id_list = [int(item) for item in users_id_list_string if item.isdecimal()]
            selected_users_to_add = User.objects.filter(id__in=users_id_list)
            users_to_add = [item for item in selected_users_to_add if item not in chat_room.users.all()]

            chat_room.users.add(*users_to_add)
            chat_room.save()

            found_users = []
            for user in users_to_add:
                full_name = f'{user.first_name} {user.last_name}'
                item = {
                    'pk': user.pk,
                    'full_name': full_name,
                    'gender': user.data.gender,
                    'profile_image_url': user.data.profile_image.image.url if user.data.profile_image else None,
                    'profile_page_url': '/' + user.site_url,
                }
                found_users.append(item)

            response = {
                'success': True,
                'usersToAdd': found_users,
            }

            return JsonResponse(response, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Chat is not group'}, status=400)


def leave_group_chat(request, uuid_url):
    if request.method == "POST":
        try:
            chat_room = ChatRoom.objects.get(uuid_url=uuid_url)
        except:
            return JsonResponse({'success': False, 'error': 'Chat not found'}, status=400)
        if chat_room.is_group:
            if len(chat_room.users.all()) > 1:
                chat_room.users.remove(request.user)
                chat_room.save()
                chat_room.change_owner(request.user)
            else:
                chat_room.delete()

            last_room = LastVisitedRoom.objects.get(user=request.user)
            last_room.room = None
            last_room.save()
            response = {
                'success': True,
                'redirect_url': r"chat/r",
            }

            return JsonResponse(response, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Chat is not group'}, status=400)


def rename_group_chat(request, uuid_url):
    if request.method == "POST":
        try:
            chat_room = ChatRoom.objects.get(uuid_url=uuid_url)
        except:
            return JsonResponse({'success': False, 'error': 'Chat not found'}, status=400)
        if chat_room.is_group:
            new_name = request.POST.get('new_name').strip()
            if len(new_name) <= 255:
                chat_room.name = new_name
                chat_room.save()
                response = {
                    'success': True,
                    'room_id': chat_room.id,
                }

                return JsonResponse(response, status=200)
            else:
                response = {
                    'success': False,
                    'error_message': 'Too long',
                }

                return JsonResponse(response, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Chat is not group'}, status=400)


def add_to_group_chat_search_result(request):
    if request.method == "POST":
        user_data = request.POST.get('userData').lower().strip()
        new_chat_check = request.POST.get('newChat')
        user_friends = Friend.objects.friends(request.user)
        user_friends_no_block = remove_blocked_users(request.user, user_friends)
        if new_chat_check == 'False':
            chat_uuid = request.POST.get('chatUuid')
            try:
                chat_room = ChatRoom.objects.get(uuid_url=chat_uuid)
                user_friends_not_in_chat = [item for item in user_friends_no_block if item not in chat_room.users.all()]
                user_friends_no_block = user_friends_not_in_chat
            except:
                return JsonResponse({'success': False, 'error': 'Chat with this uuid does not exist'}, status=400)

        matching_users_list = [item for item in user_friends_no_block if (
          (user_data in item.first_name.lower()) or (user_data in item.last_name.lower()))]

        if len(matching_users_list) > 0 and len(user_data) > 0:
            found_users = []
            for user in matching_users_list:
                full_name = f'{user.first_name} {user.last_name}'
                item = {
                    'pk': user.pk,
                    'full_name': full_name,
                    'full_name_truncate': full_name[:30],
                    'gender': user.data.gender,
                    'profile_image_url': user.data.profile_image.image.url if user.data.profile_image else None,
                }
                found_users.append(item)
        else:
            found_users = 'There is no matching friend'
        return JsonResponse({'foundUsers': found_users})
    return JsonResponse({})


def create_chat_with_user(request):
    if request.method == "POST":
        message_content = request.POST.get('message_content').strip()
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=int(user_id))
        except:
            return JsonResponse({'success': False, 'error': 'User does not exist.'}, status=400)
        chat_room = ChatRoom.objects.create(owner=request.user)
        chat_room.users.add(request.user, user)
        chat_room.save()
        Message.objects.create(
            room=chat_room,
            user=request.user,
            content=message_content,
        )
        response = {
            'success': True,
            'chat_redirect_url': r"chat/" + chat_room.uuid_url,
        }

        return JsonResponse(response, status=200)
