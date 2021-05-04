from django.db import models
from django.contrib.auth.models import User


class PageUsers(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    logo = models.ImageField(blank=True, null=True)
    background = models.ImageField(blank=True, null=True)


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
