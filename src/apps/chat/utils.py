from .models import ChatRoom


def chat_rooms_navbar_data(user):
    rooms = ChatRoom.objects.filter(users=user)
    chat_rooms = list()
    for room in rooms:
        if room.is_group:
            chat_name = room.name
            chat_image_url = '/static/images/gallery_icons/avatar-multiple-users.png'
        else:
            navbar_chat_users = room.users.all()
            if len(navbar_chat_users) == 2:
                chat_user = room.users.all()[0] if room.users.all()[0] != user else room.users.all()[1]
                chat_name = f'{chat_user.first_name} {chat_user.last_name}'
                if chat_user.data.profile_image:
                    chat_image_url = chat_user.data.profile_image.image.url
                elif chat_user.data.gender == 'male':
                    chat_image_url = '/static/images/gallery_icons/avatar-male.png'
                elif chat_user.data.gender == 'female':
                    chat_image_url = '/static/images/gallery_icons/avatar-female.png'
                else:
                    chat_image_url = '/static/images/gallery_icons/avatar-default.png'
            else:
                chat_name = room.name
                chat_image_url = '/static/images/gallery_icons/avatar-default.png'

        if last_message := room.messages.all().last():
            last_message_user_name = 'You' if last_message.user == user else last_message.user.first_name
            last_message_content = room.messages.all().last().content[:30]
        else:
            last_message_user_name = ''
            last_message_content = ''

        chat_rooms.append({
            'chat_id': room.id,
            'chat_uuid_url': room.uuid_url,
            'chat_name': chat_name,
            'chat_image_url': chat_image_url,
            'chat_is_user_deleted': room.is_user_deleted,
            'chat_date_last_message': str(room.date_last_message) if room.date_last_message else '',
            'chat_last_message_user_name': last_message_user_name,
            'chat_last_message_content': last_message_content,
            'is_new_message': True if user.id not in room.get_last_message_read_by() else False,
            'order_date': str(room.date_last_message) if room.date_last_message else str(room.created_at),
        })
    chat_rooms = sorted(chat_rooms, key=lambda item: item['order_date'], reverse=True)

    return chat_rooms
