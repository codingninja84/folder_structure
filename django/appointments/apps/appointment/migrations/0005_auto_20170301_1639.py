# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 00:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_auto_20170301_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='task',
            new_name='tasks',
        ),
    ]
