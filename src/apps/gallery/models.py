from django.db import models
from django.conf import settings
from apps.posts.models import Post

from dynamic_filenames import FilePattern
from uuid import uuid4


# Create your models here.

User = settings.AUTH_USER_MODEL


# rename file name on upload and set upload path
path_and_rename_post_image = FilePattern(
    filename_pattern='post_images/{instance.user.id}/{name}{ext}'
)

path_and_rename_temporary_image = FilePattern(
    filename_pattern='temp_post_images/{uuid:x}{ext}'
)


class Image(models.Model):
    image = models.ImageField(upload_to=path_and_rename_post_image, blank=True, null=True)
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    main_picture = models.BooleanField(default=False)
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    edit_to_delete = models.BooleanField(default=False)

    def __str__(self):
        if self.main_picture:
            return f'{self.user}-{self.id}-MAIN'
        return f'{self.user}-{self.id}_{self.image}'

    class Meta:
        ordering = ('user', '-created_at')


class TemporaryImage(models.Model):
    image = models.ImageField(upload_to=path_and_rename_temporary_image, blank=True, null=True)
    user = models.ForeignKey(User, related_name='temp_images', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='temp_images', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'TEMP_{self.user}-{self.id}'

    class Meta:
        ordering = ('user', '-created_at')


class Album(models.Model):
    title = models.CharField(max_length=100, default='No name album')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    post = models.OneToOneField(Post, related_name='albums', on_delete=models.CASCADE, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    uuid_id = models.UUIDField(default=uuid4)
    uuid_url = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.user}-{self.id}_{self.title}'

    def save(self, *args, **kwargs):
        if not self.uuid_url:
            self.uuid_url = str(self.uuid_id).replace('-', '')
        super(Album, self).save(*args, **kwargs)

    class Meta:
        ordering = ('user', '-created_at')
