# Generated by Django 4.2.6 on 2023-11-07 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_post_psot_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='psot_pic',
            new_name='post_pic',
        ),
    ]
