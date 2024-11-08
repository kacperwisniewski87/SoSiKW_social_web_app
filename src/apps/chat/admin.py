from django.contrib import admin
from .models import ChatRoom, Message, LastVisitedRoom

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    model = Message
    readonly_fields = ('date_added',)

    fieldsets = (
        (None, {'fields': ("room", "user", "user_name", "content", 'date_added',)}),
    )

    ordering = ('room', 'date_added')


class ChatRoomAdmin(admin.ModelAdmin):
    model = ChatRoom

    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ("name", "owner", "users", "is_group", 'is_user_deleted', 'date_last_message',
                           'last_message_read_by', 'uuid_id', 'uuid_url', 'created_at')}),
    )


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(LastVisitedRoom)



