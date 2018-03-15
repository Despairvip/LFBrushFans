# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_admin', '0002_client_unionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='count_project',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='pro_gold',
            field=models.DecimalField(decimal_places=10, verbose_name='积分', null=True, max_digits=19, default=Decimal('0.0')),
        ),
    ]
