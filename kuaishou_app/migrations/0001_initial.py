# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayListModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('order_id', models.CharField(max_length=200, verbose_name='订单号')),
                ('ddh', models.CharField(max_length=100, verbose_name='支付平台订单号', default='')),
                ('money', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='支付金额', default=Decimal('0.0'))),
                ('pay_list_date', models.DateTimeField(auto_now_add=True)),
                ('order_type', models.IntegerField(choices=[(0, '积分充值'), (1, '开通会员')], verbose_name='订单类型', default=0)),
                ('pay_type', models.IntegerField(choices=[(0, '支付宝支付'), (1, '微信支付')], verbose_name='支付类型', default=1)),
                ('remark', models.TextField(verbose_name='说明', default='')),
                ('status', models.IntegerField(choices=[(1, '成功'), (2, '失败'), (3, '等待付款')], verbose_name='订单状态', default=3)),
                ('client', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaveOpenId',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('open_id', models.CharField(max_length=500, null=True, default='')),
                ('open_type', models.IntegerField(choices=[(0, '微信登录'), (1, 'QQ登录')])),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
