# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 19:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_exc_api', '0022_auto_20160324_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='stock_exc_api.StockExchangeIndex'),
        ),
    ]
