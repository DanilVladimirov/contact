from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gdstorage.storage import (GoogleDriveStorage,
                               GoogleDrivePermissionType,
                               GoogleDrivePermissionRole,
                               GoogleDriveFilePermission)
permission = GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.USER,
   "danilvladimirovnkk@gmail.com"
)

gd_storage = GoogleDriveStorage(permissions=(permission,))


class PageUsers(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=None)
    logo = models.ImageField(upload_to='logos', storage=gd_storage, null=True, blank=True)
    background = models.ImageField(upload_to='backgrounds', storage=gd_storage, blank=True, null=True)


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
