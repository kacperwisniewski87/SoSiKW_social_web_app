import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, ChatRoom

from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
        self.room_group_name = 'chat_%s' % self.room_uuid

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']
        user_name = data['user_name']
        user_full_name = data['user_full_name']
        room_uuid = data['room_uuid']

        if message:
            await self.save_message(user_id, room_uuid, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': user_id,
                    'user_name': user_name,
                    'user_full_name': user_full_name,
                    'room_uuid': room_uuid,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_name = event['user_name']
        user_full_name = event['user_full_name']
        room_uuid = event['room_uuid']

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'user_name': user_name,
            'user_full_name': user_full_name,
            'room_uuid': room_uuid,
        }))

    @sync_to_async
    def save_message(self, userid, room_uuid, message):
        user = User.objects.get(id=int(userid))
        chat_room = ChatRoom.objects.get(uuid_url=room_uuid)
        message = Message.objects.create(user=user, room=chat_room, content=message)

        chat_room.date_last_message = message.date_added
        chat_room.set_last_message_read_by([userid])
        chat_room.save()
