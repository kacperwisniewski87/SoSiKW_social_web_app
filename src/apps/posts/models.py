from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')
    published_date = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.id}_{self.user.first_name}_{self.id}:{self.text[:100]}...'

    class Meta:
        ordering = ('-published_date', )


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class CommentReply(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='comments_reply')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class SecondaryCommentReply(models.Model):
    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE, related_name='secondary_reply')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

