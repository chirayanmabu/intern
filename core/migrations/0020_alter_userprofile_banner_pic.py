# Generated by Django 4.2.6 on 2023-11-09 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='banner_pic',
            field=models.ImageField(blank=True, default='banner_default.png', null=True, upload_to='banner_pictures/'),
        ),
    ]
