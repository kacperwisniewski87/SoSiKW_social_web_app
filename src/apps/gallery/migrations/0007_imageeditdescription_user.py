# Generated by Django 4.2.7 on 2024-04-25 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '0006_imageeditdescription_to_delete_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageeditdescription',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='edit_image_description', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]