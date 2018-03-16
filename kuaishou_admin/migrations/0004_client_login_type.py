# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_admin', '0003_auto_20180314_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='login_type',
            field=models.IntegerField(default=0),
        ),
    ]
