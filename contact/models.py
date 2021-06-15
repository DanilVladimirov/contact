import os
import random

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    return f'{basefilename}_{randomstr}{file_extension}'


class ImagesUser(models.Model):
    title = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return self.title


class PageUsers(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    logo = models.ImageField(upload_to=photo_path, null=True, blank=True, default='default-user.jpeg')
    background = models.ImageField(upload_to=photo_path, blank=True, null=True)
    imgs = models.ManyToManyField(ImagesUser)
    publics = models.ManyToManyField('Public')


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
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.label


class Follows(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    another_user = models.ManyToManyField(User, related_name='another_user')


class Followers(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE, related_name='user')
    another_users = models.ManyToManyField(User, related_name='another_users')


class Message(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


class Room(models.Model):
    name = models.CharField(max_length=255)
    messages = models.ManyToManyField(Message)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user2')

    def __str__(self):
        return self.name


class Types(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Public(models.Model):
    title = models.CharField(max_length=200, default='noname')
    logo = models.ImageField(upload_to=photo_path)
    desc = models.TextField(default='')
    background = models.ImageField(upload_to=photo_path)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    moders = models.ManyToManyField(User, blank=True, related_name='moders')
    admins = models.ManyToManyField(User, blank=True, related_name='admins')
    posts = models.ManyToManyField(Post, blank=True)
    imgs = models.ManyToManyField(ImagesUser, blank=True)
    type_public = models.ForeignKey(Types, on_delete=models.CASCADE, null=True)
    black_list = models.ManyToManyField(User, related_name='black_list')

    def __str__(self):
        return self.title
