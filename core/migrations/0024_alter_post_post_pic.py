# Generated by Django 4.2.6 on 2023-11-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_post_post_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_pic',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
