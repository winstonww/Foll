# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foll', '0031_auto_20160724_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='location',
            field=models.CharField(max_length=500),
        ),
    ]
