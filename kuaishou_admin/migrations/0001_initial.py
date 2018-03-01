# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user_id', models.CharField(default='', max_length=20)),
                ('consume_gold', models.IntegerField()),
                ('phone_num', models.IntegerField()),
                ('gold', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'kuaishou_client',
            },
        ),
        migrations.CreateModel(
            name='Old_Order_project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('old_gold', models.DecimalField(max_digits=19, verbose_name='积分', decimal_places=10, default=Decimal('0.0'))),
            ],
            options={
                'db_table': 'kuaishou_expend_ord',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('gold', models.DecimalField(max_digits=19, verbose_name='积分', decimal_places=10, default=Decimal('0.0'))),
                ('data', models.TextField(default='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('showdata', models.TextField(default='')),
                ('count_init', models.IntegerField(default=0)),
                ('type_id', models.IntegerField(default=0)),
                ('kuaishou_id', models.CharField(max_length=20)),
                ('link_works', models.URLField()),
                ('status', models.IntegerField(choices=[(0, '未开始'), (1, '执行中'), (2, '已完成'), (3, '异常单'), (4, '已撤单')], default=0)),
                ('order_id_num', models.CharField(max_length=20)),
                ('client', models.ForeignKey(to='kuaishou_admin.Client')),
            ],
            options={
                'db_table': 'kuaishou_order',
            },
        ),
        migrations.CreateModel(
            name='Order_combo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('pro_gold', models.DecimalField(max_digits=19, verbose_name='积分', decimal_places=10, default=Decimal('0.0'))),
            ],
            options={
                'db_table': 'kuaishou_combo',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('pro_name', models.CharField(max_length=100)),
                ('count_project', models.IntegerField()),
                ('pro_gold', models.DecimalField(max_digits=19, verbose_name='积分', decimal_places=10, default=Decimal('0.0'))),
                ('combo', models.ManyToManyField(to='kuaishou_admin.Order_combo', blank=True)),
            ],
            options={
                'db_table': 'kuaishou_project',
            },
        ),
        migrations.AddField(
            model_name='order_combo',
            name='detail_combo',
            field=models.ManyToManyField(to='kuaishou_admin.Project', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(to='kuaishou_admin.Project'),
        ),
        migrations.AddField(
            model_name='old_order_project',
            name='orders',
            field=models.OneToOneField(null=True, to='kuaishou_admin.Order'),
        ),
    ]
