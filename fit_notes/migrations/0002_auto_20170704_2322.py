# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 20:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit_notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='Duration of exercise'),
            preserve_default=False,
        ),
    ]
