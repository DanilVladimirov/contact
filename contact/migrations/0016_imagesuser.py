# Generated by Django 3.1.7 on 2021-06-12 16:31

import contact.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0015_post_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('img', models.ImageField(upload_to=contact.models.photo_path)),
            ],
        ),
    ]
