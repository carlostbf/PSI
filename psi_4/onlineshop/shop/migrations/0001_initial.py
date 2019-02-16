# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 16:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catName', models.CharField(max_length=128, unique=True)),
                ('catSlug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodName', models.CharField(max_length=128, unique=True)),
                ('prodSlug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='images/products')),
                ('description', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=1)),
                ('availability', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2017, 10, 27, 16, 0, 40, 322827, tzinfo=utc))),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
            ],
        ),
    ]