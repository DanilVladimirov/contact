# Generated by Django 3.1.7 on 2021-05-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_auto_20210508_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageusers',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pageusers',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
