# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2024-08-18 17:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='is_nav',
        ),
    ]
