import decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Client(AbstractUser):
    choices_login_type = (
        (0, "微信登陆"),
        (1, 'qq登陆')
    )
    hands_id = models.CharField(max_length=20, default='')
    # 总消费
    consume_gold = models.IntegerField(default=0)
    # 联系方式
    phone_num = models.CharField(max_length=15, blank=True, null=True)
    # 金币
    gold = models.IntegerField(default=0)
    # 用户名
    # name = models.CharField(max_length=20, default=0)

    avatar = models.CharField(max_length=500, default='', null=True)

    token = models.CharField(max_length=500, default='')
    unionid = models.CharField(max_length=500, default='', null=True)
    login_type = models.IntegerField(default=0, choices=choices_login_type)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.username

    def to_dict(self):
        dict = {
            "user_id": self.id,
            "user_name": (self.username).split(".")[0],
            "gold": self.gold,
            "phone_num": self.phone_num,
            "consume_gold": self.consume_gold,
            "avatar": self.avatar
        }
        return dict

    class Meta:
        db_table = "kuaishou_client"


class Project(models.Model):
    '''
    项目表
    '''
    pro_name = models.CharField(max_length=100, blank=False)
    count_project = models.IntegerField(default=0)
    pro_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'), null=True)

    def to_dict(self):
        data = {
            "pro_id": self.id,
            "pro_count": self.count_project,
            "pro_gold": self.pro_gold,
        }
        return data

    def __str__(self):
        return self.pro_name

    class Meta:
        db_table = "kuaishou_project"


class Order(models.Model):
    '''
    订单表
    '''
    choices_status = (
        (0, "所有类型"),
        (1, "未开始"),
        (2, "执行中"),
        (3, "已完成"),
        (4, "异常单"),
        (5, "已撤单"),
    )
    choices_pays = (
        (0, "支付宝支付"),
        (1, "微信支付"),
    )
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', blank=True, null=True, default='', on_delete=models.CASCADE)
    combo = models.ForeignKey('Order_combo', blank=True, null=True, default='', on_delete=models.CASCADE)

    gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))
    data = models.TextField(default="")
    create_date = models.DateTimeField(auto_now_add=True)
    showdata = models.TextField(default="")
    count_init = models.IntegerField(default=0)
    type_id = models.IntegerField(default=0)
    kuaishou_id = models.CharField(max_length=20, default='')
    link_works = models.URLField(blank=True, default='')
    status = models.IntegerField(default=1, choices=choices_status)
    order_id_num = models.CharField(max_length=2000)

    def __str__(self):
        return self.kuaishou_id

    def to_dict(self):
        status = self.status
        if status == 1:
            fettle = '未开始'
        elif status == 2:
            fettle = "执行中"
        elif status == 3:
            fettle = "已完成"
        elif status == 4:
            fettle = '异常单'
        else:
            fettle = "以撤单"
        order_dict = {

            "order_id": self.order_id_num,
            # "project_name": self.project.pro_name,
            "kuaishou_id": self.kuaishou_id,
            "ordered_num": self.count_init,
            "work_links": self.link_works,
            "status_order": fettle,

            "user_name": self.client.username,
            "create_order_time": self.create_date
        }
        return order_dict

    class Meta:
        db_table = "kuaishou_order"


class Combo_project(models.Model):
    '''
    套餐所关联的项目
    '''
    pro_name = models.CharField(max_length=100, null=False)
    count_project = models.IntegerField(default=0)
    pro_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'), null=True)

    def __str__(self):
        return self.pro_name

    class Meta:
        db_table = "combo_project"


class Order_combo(models.Model):
    '''
    套餐表
    '''
    name = models.CharField(max_length=100, null=False)
    detail_combo = models.ManyToManyField('Project', blank=True)
    pro_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))
    project_detail = models.ManyToManyField('Combo_project')

    def to_dict(self):
        data = {
            "pro_id": self.id,
            "pro_name": self.name,
            "pro_gold": self.pro_gold,
        }
        return data

    def __str__(self):
        return self.name

    class Meta:
        db_table = "kuaishou_combo"


class Old_Order_project(models.Model):
    '''
    扩展表  历史记录表
    '''
    old_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))

    orders = models.OneToOneField('Order', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "kuaishou_expend_ord"


class AdminManagement(models.Model):
    # choice_delete = (
    #     (0, "正常"),
    #     (1, "删除")
    # )
    wechat = models.CharField(max_length=100, default='', null=True)

    def __str__(self):
        return self.wecaht

    class Meta:
        db_table = "admin_id"


class CheckVersion(models.Model):
    version = models.CharField(max_length=100, default=1)
    sdk_url = models.CharField(max_length=500, default='1')
    update_msg = models.CharField(max_length=1000, default='1')

    def __str__(self):
        return self.version

    class Meta:
        db_table = "version_num"


class MoneyAndGold(models.Model):
    """
    设置金钱和积分的对应关系表
    """
    gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))#积分
    money = models.DecimalField("金钱", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))#金钱

