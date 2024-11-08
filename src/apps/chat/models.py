from django.db import models
from django.conf import settings

import json

from uuid import uuid4


User = settings.AUTH_USER_MODEL


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    is_group = models.BooleanField(default=False)
    is_user_deleted = models.BooleanField(default=False)
    date_last_message = models.DateTimeField(auto_now_add=False, blank=True, null=True, default=None)
    last_message_read_by = models.JSONField(default="[]")
    uuid_id = models.UUIDField(default=uuid4)
    uuid_url = models.CharField(max_length=32)

    class Meta:
        ordering = ('-date_last_message',)

    def __str__(self):
        if not self.is_group and self.name:
            return f'{self.uuid_url} - [DELETED] {self.name}'
        return f'{self.uuid_url} - {self.name}' if self.name else f'{self.uuid_url} - {list(self.users.all())}'

    def save(self, *args, **kwargs):
        if not self.uuid_url:
            self.uuid_url = str(self.uuid_id).replace('-', '')
        super(ChatRoom, self).save(*args, **kwargs)

    def set_last_message_read_by(self, u):
        self.last_message_read_by = json.dumps(u)

    def get_last_message_read_by(self):
        return json.loads(self.last_message_read_by)

    def change_owner(self, check_user):
        if check_user == self.owner:
            for item in self.users.all():
                if item != check_user:
                    self.owner = item
                    break
            self.save()

    def set_name_upon_user_deletion(self, deleted_user):
        self.is_user_deleted = True
        self.name = f'{deleted_user.first_name} {deleted_user.last_name}'
        self.save()


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=60, blank=True, null=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('room', 'date_added')

    def __str__(self):
        if self.user:
            return f'({self.room.uuid_url})({self.user.first_name} {self.user.last_name})-> {self.content[:40]}'
        else:
            return f'({self.room.uuid_url})({self.user_name})-> {self.content[:40]}'

    def set_deleted_user_name(self, deleted_user):
        self.user_name = f'{deleted_user.first_name} {deleted_user.last_name}'
        self.save()


class LastVisitedRoom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.id}-{self.user.first_name} {self.user.last_name} - {self.room}'

    def set_visited_room(self, room):
        if Message.objects.filter(room=room):
            self.room = room
            self.save()
