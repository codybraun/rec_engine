# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-01 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rec_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rec',
            unique_together=set([('product', 'user')]),
        ),
    ]
