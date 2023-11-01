from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(default="", null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    def __str__(self):
        return self.username