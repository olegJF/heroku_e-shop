# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-29 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20170313_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='measurement',
            field=models.CharField(choices=[('pcs', 'шт.'), ('kg', 'кг.'), ('l', 'л.')], default='pcs', max_length=10, verbose_name='измерение'),
        ),
        migrations.AddField(
            model_name='product',
            name='value',
            field=models.FloatField(default=0, verbose_name='зачение'),
        ),
    ]
