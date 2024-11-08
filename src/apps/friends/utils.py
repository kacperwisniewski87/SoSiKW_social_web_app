import json
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from friendship.models import Block, Friend

User = get_user_model()


def remove_blocked_users(user, user_list):
    """Remove blocked and blocking users from queryset"""

    users_with_block = set(Block.objects.blocked(user)) | set(Block.objects.blocking(user))
    result = list(set(user_list).difference(users_with_block))
    return result


def remove_blocked_users_from_requests(user, friendship_requests, request_type=None):
    """Remove blocked and blocking users from friendship requests queryset"""

    users_with_block = set(Block.objects.blocked(user)) | set(Block.objects.blocking(user))
    if request_type == 'sent':
        result = [invitation for invitation in friendship_requests if invitation.to_user not in users_with_block]
    else:
        result = [invitation for invitation in friendship_requests if invitation.from_user not in users_with_block]

    return result


def remove_friend_users(user, user_list):
    """Remove friends from queryset"""

    friends = set(Friend.objects.friends(user))
    friends.add(user)
    result = list(set(user_list).difference(friends))
    return result


def unrejected_request_count_without_blocked_users(user):
    friendship_requests = Friend.objects.unrejected_requests(user=user)
    users_with_block = set(Block.objects.blocked(user)) | set(Block.objects.blocking(user))
    result = len([invitation for invitation in friendship_requests if invitation.from_user not in users_with_block])
    return result


def custom_user_list_serializer(users_list):
    users_list_data = json.loads(serialize('json', users_list))
    redundant_fields = ['password', 'is_superuser', 'is_active', 'is_staff', 'date_joined', 'groups',
                        'user_permissions', 'last_login']
    for user_item_data in users_list_data:
        for item in redundant_fields:
            user_item_data['fields'].pop(item)
        user = User.objects.get(pk=user_item_data['pk'])
        profile_data = user.data
        if profile_data.profile_image:
            user_item_data['fields']['profile_image_url'] = profile_data.profile_image.image.url
        else:
            user_item_data['fields']['profile_image_url'] = None
        user_item_data['fields']['gender'] = profile_data.gender
    return json.dumps(users_list_data, cls=DjangoJSONEncoder)
