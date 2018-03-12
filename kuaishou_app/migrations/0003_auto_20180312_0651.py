# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_app', '0002_auto_20180311_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paylistmodel',
            name='client',
        ),
        migrations.DeleteModel(
            name='PayListModel',
        ),
    ]
