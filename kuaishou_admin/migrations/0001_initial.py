# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('hands_id', models.CharField(max_length=20, default='')),
                ('consume_gold', models.IntegerField(default=0)),
                ('phone_num', models.CharField(max_length=15, null=True, blank=True)),
                ('gold', models.IntegerField(default=0)),
                ('avatar', models.CharField(max_length=500, null=True, default='')),
                ('token', models.CharField(max_length=500, default='')),
                ('unionid', models.CharField(max_length=500, null=True, default='')),
                ('login_type', models.IntegerField(choices=[(0, '微信登陆'), (1, 'qq登陆')], default=0)),
                ('version', models.IntegerField(default=1)),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set', blank=True, to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set', blank=True, to='auth.Permission')),
            ],
            options={
                'db_table': 'kuaishou_client',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdminManagement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('wechat', models.CharField(max_length=100, null=True, default='')),
            ],
            options={
                'db_table': 'admin_id',
            },
        ),
        migrations.CreateModel(
            name='CheckVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('version', models.CharField(max_length=100, default=1)),
            ],
            options={
                'db_table': 'version_num',
            },
        ),
        migrations.CreateModel(
            name='Combo_project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('pro_name', models.CharField(max_length=100)),
                ('count_project', models.IntegerField(default=0)),
                ('pro_gold', models.DecimalField(decimal_places=10, max_digits=19, null=True, verbose_name='积分', default=Decimal('0.0'))),
            ],
            options={
                'db_table': 'combo_project',
            },
        ),
        migrations.CreateModel(
            name='Old_Order_project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('old_gold', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='积分', default=Decimal('0.0'))),
            ],
            options={
                'db_table': 'kuaishou_expend_ord',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('gold', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='积分', default=Decimal('0.0'))),
                ('data', models.TextField(default='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('showdata', models.TextField(default='')),
                ('count_init', models.IntegerField(default=0)),
                ('type_id', models.IntegerField(default=0)),
                ('kuaishou_id', models.CharField(max_length=20, default='')),
                ('link_works', models.URLField(blank=True, default='')),
                ('status', models.IntegerField(choices=[(0, '所有类型'), (1, '未开始'), (2, '执行中'), (3, '已完成'), (4, '异常单'), (5, '已撤单')], default=1)),
                ('order_id_num', models.CharField(max_length=2000)),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kuaishou_order',
            },
        ),
        migrations.CreateModel(
            name='Order_combo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('pro_gold', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='积分', default=Decimal('0.0'))),
            ],
            options={
                'db_table': 'kuaishou_combo',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('pro_name', models.CharField(max_length=100)),
                ('count_project', models.IntegerField(default=0)),
                ('pro_gold', models.DecimalField(decimal_places=10, max_digits=19, null=True, verbose_name='积分', default=Decimal('0.0'))),
                ('img_url', models.CharField(max_length=100, default='')),
            ],
            options={
                'db_table': 'kuaishou_project',
            },
        ),
        migrations.AddField(
            model_name='order_combo',
            name='detail_combo',
            field=models.ManyToManyField(blank=True, to='kuaishou_admin.Project'),
        ),
        migrations.AddField(
            model_name='order_combo',
            name='project_detail',
            field=models.ManyToManyField(to='kuaishou_admin.Combo_project'),
        ),
        migrations.AddField(
            model_name='order',
            name='combo',
            field=models.ForeignKey(null=True, default='', blank=True, to='kuaishou_admin.Order_combo'),
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(null=True, default='', blank=True, to='kuaishou_admin.Project'),
        ),
        migrations.AddField(
            model_name='old_order_project',
            name='orders',
            field=models.OneToOneField(null=True, to='kuaishou_admin.Order'),
        ),
    ]
