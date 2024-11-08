from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.chat.models import LastVisitedRoom


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **kwargs):
        """
        Create and save a user with given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set.'))
        kwargs['site_url'] = f'{kwargs.get("first_name")}.{kwargs.get("last_name")}'.lower()
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        LastVisitedRoom.objects.create(user=user)

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and save SuperUser with given email and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **kwargs)
