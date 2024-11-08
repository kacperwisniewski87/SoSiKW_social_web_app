from django.contrib import admin
from .models import Album, Image, TemporaryImage

# Register your models here.

admin.site.register(Album)
admin.site.register(Image)
admin.site.register(TemporaryImage)
