# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 19:12
from __future__ import unicode_literals

from django.db import migrations
import file_storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('file_storage', '0010_auto_20170319_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='file_name',
            field=file_storage.models.CustomImageField(upload_to=b'dummy'),
        ),
    ]
