from django.contrib import admin

from .models import *

admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(FriendRequest)
admin.site.register(Comment)