# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_storage', '0011_auto_20170319_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='file_name',
            field=models.TextField(),
        ),
    ]
