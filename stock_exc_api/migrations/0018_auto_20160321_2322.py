# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_exc_api', '0017_auto_20160321_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, default='Brazil', max_length=100),
        ),
    ]
