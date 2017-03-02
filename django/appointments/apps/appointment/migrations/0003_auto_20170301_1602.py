# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 00:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_user_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 0, 1, 38, 221000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='task',
            field=models.CharField(default='test', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to='appointment.User'),
            preserve_default=False,
        ),
    ]