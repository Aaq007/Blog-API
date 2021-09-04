from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)

# admin.site.register(UserAdmin)
