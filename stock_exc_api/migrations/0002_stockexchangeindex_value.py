# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_exc_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockexchangeindex',
            name='value',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
