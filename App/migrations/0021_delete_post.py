# Generated by Django 4.2.4 on 2023-10-11 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_rename_timestamp_post_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
