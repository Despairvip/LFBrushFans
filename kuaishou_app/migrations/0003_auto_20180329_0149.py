# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-29 01:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_app', '0002_auto_20180327_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paylistmodel',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pay_order', to=settings.AUTH_USER_MODEL),
        ),
    ]