# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_secrets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secret',
            name='likes',
        ),
        migrations.AddField(
            model_name='secret',
            name='liked_by',
            field=models.ManyToManyField(related_name='Likes', to='dojo_secrets.User'),
        ),
    ]
