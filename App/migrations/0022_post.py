# Generated by Django 4.2.4 on 2023-10-11 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0021_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
