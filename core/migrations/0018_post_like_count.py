# Generated by Django 4.2.6 on 2023-11-09 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.BigIntegerField(default='0'),
        ),
    ]
