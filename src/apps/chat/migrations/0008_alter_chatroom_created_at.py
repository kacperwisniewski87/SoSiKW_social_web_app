# Generated by Django 4.2.7 on 2024-10-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_chatroom_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
