import os
import random

from django.db import models
from django.contrib.auth.models import User


def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    return f'{basefilename}_{randomstr}{file_extension}'


class PageUsers(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    logo = models.ImageField(upload_to=photo_path, null=True, blank=True, default='default-user.jpeg')
    background = models.ImageField(upload_to=photo_path, blank=True, null=True)


class CommentsPost(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    text = models.TextField(default='Текст')


class Post(models.Model):
    label = models.TextField(default='Тема')
    text = models.TextField(default='Текст')
    page = models.ForeignKey(PageUsers,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    comments = models.ManyToManyField(CommentsPost)


class Follows(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    another_user = models.ManyToManyField(User, related_name='another_user')



