# Generated by Django 4.2.4 on 2023-10-20 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0071_rename_text_comment_comment_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_text',
            new_name='text',
        ),
    ]
