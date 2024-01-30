# Generated by Django 4.2.4 on 2023-10-05 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_remove_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='website_link',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website_link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
