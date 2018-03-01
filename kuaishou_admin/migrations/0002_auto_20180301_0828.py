# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_admin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='user_id',
            new_name='wechat_id',
        ),
    ]
