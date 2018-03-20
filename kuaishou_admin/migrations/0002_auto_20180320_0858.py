# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_admin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='img_url',
        ),
        migrations.AddField(
            model_name='project',
            name='pro_type',
            field=models.IntegerField(default=1, choices=[(1, '刷粉丝'), (2, '刷双击'), (3, '刷播放')]),
        ),
    ]
