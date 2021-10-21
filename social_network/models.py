from django.db import models
from django.contrib.auth.models import AbstractUser

from core import settings


class User(AbstractUser):
    last_login = models.DateTimeField('Last Login', blank=True, null=True)
    last_request = models.DateTimeField('Last Request', blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField('Title', max_length=256, unique=True)
    content = models.TextField('Content', blank=True, null=True)
    likes = models.IntegerField('Likes', default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Owner', on_delete=models.CASCADE)
    publish_date = models.DateTimeField('Publish Date', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    publish_date = models.DateField('Liked Date', auto_now_add=True, blank=True, null=True)
