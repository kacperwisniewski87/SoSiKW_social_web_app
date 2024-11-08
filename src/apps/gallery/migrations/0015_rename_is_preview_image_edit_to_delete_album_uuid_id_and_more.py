# Generated by Django 4.2.7 on 2024-05-19 09:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_text_alter_temporarypost_text'),
        ('gallery', '0014_alter_temporaryimage_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='is_preview',
            new_name='edit_to_delete',
        ),
        migrations.AddField(
            model_name='album',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='temporaryimage',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temp_images', to='posts.post'),
        ),
    ]
