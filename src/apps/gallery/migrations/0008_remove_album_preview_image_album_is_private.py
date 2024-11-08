# Generated by Django 4.2.7 on 2024-05-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_imageeditdescription_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='preview_image',
        ),
        migrations.AddField(
            model_name='album',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]