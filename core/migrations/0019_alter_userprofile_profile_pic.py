# Generated by Django 4.2.6 on 2023-11-09 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_post_like_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_picture.png', null=True, upload_to='profile_pictures/'),
        ),
    ]
