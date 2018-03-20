# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_admin', '0002_auto_20180318_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
