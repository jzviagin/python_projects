# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 18:31
from __future__ import unicode_literals

from django.db import migrations
import file_storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('file_storage', '0008_auto_20170319_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='file_name',
            field=file_storage.models.CustomFileField(upload_to=b'photos'),
        ),
    ]
