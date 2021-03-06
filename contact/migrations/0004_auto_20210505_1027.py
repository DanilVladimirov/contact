# Generated by Django 3.1.7 on 2021-05-05 10:27

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20210505_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageusers',
            name='background',
            field=models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(permissions=(gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['READER'], gdstorage.storage.GoogleDrivePermissionType['DOMAIN'], 'contactguys.herokuapp.com'),)), upload_to='backgrounds'),
        ),
        migrations.AlterField(
            model_name='pageusers',
            name='logo',
            field=models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(permissions=(gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['READER'], gdstorage.storage.GoogleDrivePermissionType['DOMAIN'], 'contactguys.herokuapp.com'),)), upload_to='logos'),
        ),
    ]
