# Generated by Django 4.2.6 on 2023-11-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_userinfo_banner_pic_alter_userinfo_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]