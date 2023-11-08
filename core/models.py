from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserInfo(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)

    email=models.CharField(max_length=200)

    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(default="default_picture.png", upload_to='images/',null=True, blank=True)
    banner_pic = models.ImageField(default="banner_default.png", upload_to='images/',null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    friends = models.ManyToManyField('UserInfo', blank=True)

    def __str__(self):
        return self.username
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserInfo, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserInfo, related_name="to_user", on_delete=models.CASCADE)


class Post(models.Model):
    body = models.TextField()
    post_pic = models.ImageField(upload_to='images/', null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)