# Generated by Django 4.2.4 on 2023-10-17 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0053_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
