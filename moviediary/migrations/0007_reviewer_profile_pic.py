# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-14 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviediary', '0006_auto_20160611_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewer',
            name='profile_pic',
            field=models.CharField(default='amelie.jpg', max_length=20),
        ),
    ]