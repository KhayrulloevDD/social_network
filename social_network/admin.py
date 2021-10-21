from django.contrib import admin
from .models import User, Post, Like


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login', 'last_request']
    ordering = ['id']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'likes', 'owner', 'publish_date']
    ordering = ['id']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'publish_date']
    ordering = ['id']
