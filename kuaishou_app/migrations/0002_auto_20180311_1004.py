# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaishou_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paylistmodel',
            name='order_type',
            field=models.IntegerField(default=0, verbose_name='订单类型', choices=[(0, '积分充值'), (1, '开通会员')]),
        ),
        migrations.AlterField(
            model_name='paylistmodel',
            name='pay_type',
            field=models.IntegerField(default=0, verbose_name='支付类型'),
        ),
    ]
