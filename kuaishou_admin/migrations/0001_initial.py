# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from decimal import Decimal
import django.utils.timezone
import django.contrib.auth.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('hands_id', models.CharField(default='', max_length=20)),
                ('consume_gold', models.IntegerField(default=0)),
                ('phone_num', models.CharField(null=True, max_length=15, blank=True)),
                ('gold', models.IntegerField(default=0)),
                ('avatar', models.CharField(null=True, max_length=500, default='')),
                ('token', models.CharField(default='', max_length=500)),
                ('unionid', models.CharField(default='', max_length=500)),
                ('login_type', models.IntegerField(default=0, choices=[(0, '微信登陆'), (1, 'qq登陆')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', blank=True, verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', help_text='Specific permissions for this user.', to='auth.Permission', blank=True, verbose_name='user permissions')),
            ],
            options={
                'db_table': 'kuaishou_client',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Old_Order_project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('old_gold', models.DecimalField(default=Decimal('0.0'), max_digits=19, decimal_places=10, verbose_name='积分')),
            ],
            options={
                'db_table': 'kuaishou_expend_ord',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('gold', models.DecimalField(default=Decimal('0.0'), max_digits=19, decimal_places=10, verbose_name='积分')),
                ('data', models.TextField(default='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('showdata', models.TextField(default='')),
                ('count_init', models.IntegerField(default=0)),
                ('type_id', models.IntegerField(default=0)),
                ('kuaishou_id', models.CharField(default='', max_length=20)),
                ('link_works', models.URLField(default='', blank=True)),
                ('status', models.IntegerField(default=1, choices=[(0, '所有类型'), (1, '未开始'), (2, '执行中'), (3, '已完成'), (4, '异常单'), (5, '已撤单')])),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pro_gold', models.DecimalField(default=Decimal('0.0'), max_digits=19, decimal_places=10, verbose_name='积分')),
            ],
            options={
                'db_table': 'kuaishou_combo',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=100)),
                ('count_project', models.IntegerField(default=0)),
                ('pro_gold', models.DecimalField(null=True, decimal_places=10, verbose_name='积分', max_digits=19, default=Decimal('0.0'))),
                ('img_url', models.CharField(default='', max_length=100)),
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
            name='combo',
            field=models.ForeignKey(null=True, default='', to='kuaishou_admin.Order_combo', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(null=True, default='', to='kuaishou_admin.Project', blank=True),
        ),
        migrations.AddField(
            model_name='old_order_project',
            name='orders',
            field=models.OneToOneField(null=True, to='kuaishou_admin.Order'),
        ),
    ]
