# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20171027_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='catSlug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
