# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models
from decimal import Decimal
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'}, max_length=30)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('hands_id', models.CharField(default='', max_length=20)),
                ('consume_gold', models.IntegerField(default=0)),
                ('phone_num', models.CharField(blank=True, null=True, max_length=15)),
                ('gold', models.IntegerField(default=0)),
                ('avatar', models.CharField(null=True, default='', max_length=500)),
                ('token', models.CharField(default='', max_length=500)),
                ('unionid', models.CharField(null=True, default='', max_length=500)),
                ('login_type', models.IntegerField(choices=[(0, '微信登陆'), (1, 'qq登陆')], default=0)),
                ('version', models.IntegerField(default=1)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', related_name='user_set', verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', related_name='user_set', verbose_name='user permissions', to='auth.Permission', blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wechat', models.CharField(null=True, default='', max_length=100)),
            ],
            options={
                'db_table': 'admin_id',
            },
        ),
        migrations.CreateModel(
            name='CheckVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default=1, max_length=100)),
                ('sdk_url', models.CharField(default='1', max_length=500)),
                ('update_msg', models.CharField(default='1', max_length=1000)),
            ],
            options={
                'db_table': 'version_num',
            },
        ),
        migrations.CreateModel(
            name='Combo_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=100)),
                ('count_project', models.IntegerField(default=0)),
                ('pro_gold', models.DecimalField(null=True, decimal_places=10, default=Decimal('0.0'), verbose_name='积分', max_digits=19)),
            ],
            options={
                'db_table': 'combo_project',
            },
        ),
        migrations.CreateModel(
            name='Old_Order_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_gold', models.DecimalField(decimal_places=10, default=Decimal('0.0'), verbose_name='积分', max_digits=19)),
            ],
            options={
                'db_table': 'kuaishou_expend_ord',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gold', models.DecimalField(decimal_places=10, default=Decimal('0.0'), verbose_name='积分', max_digits=19)),
                ('data', models.TextField(default='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('showdata', models.TextField(default='')),
                ('count_init', models.IntegerField(default=0)),
                ('type_id', models.IntegerField(default=0)),
                ('kuaishou_id', models.CharField(default='', max_length=20)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pro_gold', models.DecimalField(decimal_places=10, default=Decimal('0.0'), verbose_name='积分', max_digits=19)),
            ],
            options={
                'db_table': 'kuaishou_combo',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=100)),
                ('count_project', models.IntegerField(default=0)),
                ('pro_gold', models.DecimalField(null=True, decimal_places=10, default=Decimal('0.0'), verbose_name='积分', max_digits=19)),
                ('pro_type', models.IntegerField(choices=[(1, '刷粉丝'), (2, '刷双击'), (3, '刷播放')], default=1)),
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
            model_name='order_combo',
            name='project_detail',
            field=models.ManyToManyField(to='kuaishou_admin.Combo_project'),
        ),
        migrations.AddField(
            model_name='order',
            name='combo',
            field=models.ForeignKey(to='kuaishou_admin.Order_combo', null=True, default='', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(to='kuaishou_admin.Project', null=True, default='', blank=True),
        ),
        migrations.AddField(
            model_name='old_order_project',
            name='orders',
            field=models.OneToOneField(to='kuaishou_admin.Order', null=True),
        ),
    ]
