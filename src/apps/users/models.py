from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from apps.gallery.models import Image
from apps.chat.models import ChatRoom, Message, LastVisitedRoom


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    site_url = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.id}_{self.first_name}_{self.last_name}'

    def delete(self, *args, **kwargs):
        messages = Message.objects.filter(user=self)
        for message in messages:
            message.set_deleted_user_name(self)
        rooms = ChatRoom.objects.filter(models.Q(users=self) & models.Q(is_group=False))
        for room in rooms:
            room.change_owner(self)
            if not room.is_group:
                room.set_name_upon_user_deletion(self)
        super(CustomUser, self).delete(*args, **kwargs)


class UserProfile(models.Model):
    GENDER_CHOICES = [('male', 'male'), ('female', 'female'), ('other', 'other')]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='data')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True, choices=GENDER_CHOICES)
    place_of_live = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.OneToOneField(Image, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('user', )

    def __str__(self):
        return f'{self.user.id}_{self.user}'
