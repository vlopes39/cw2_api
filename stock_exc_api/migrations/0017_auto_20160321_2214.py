# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_exc_api', '0016_auto_20160320_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historical_data',
            name='index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='index', to='stock_exc_api.StockExchangeIndex'),
        ),
    ]
