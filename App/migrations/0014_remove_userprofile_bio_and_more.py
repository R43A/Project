# Generated by Django 4.2.4 on 2023-10-05 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_customuser_bio_customuser_website_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website_link',
        ),
    ]
