# Generated by Django 4.2.6 on 2023-11-07 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_userinfo_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, default='banner_default.png', null=True, upload_to='images/'),
        ),
    ]
