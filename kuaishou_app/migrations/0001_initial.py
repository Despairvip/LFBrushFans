# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(verbose_name='订单号', max_length=200)),
                ('ddh', models.CharField(default='', verbose_name='支付平台订单号', max_length=100)),
                ('money', models.DecimalField(decimal_places=10, default=Decimal('0.0'), verbose_name='支付金额', max_digits=19)),
                ('pay_list_date', models.DateTimeField(auto_now_add=True)),
                ('order_type', models.IntegerField(choices=[(0, '积分充值'), (1, '开通会员')], default=0, verbose_name='订单类型')),
                ('pay_type', models.IntegerField(choices=[(0, '支付宝支付'), (1, '微信支付')], default=1, verbose_name='支付类型')),
                ('remark', models.TextField(default='', verbose_name='说明')),
                ('status', models.IntegerField(choices=[(1, '成功'), (2, '失败'), (3, '等待付款')], default=3, verbose_name='订单状态')),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaveOpenId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(null=True, default='', max_length=500)),
                ('open_type', models.IntegerField(choices=[(0, '微信登录'), (1, 'QQ登录')])),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
