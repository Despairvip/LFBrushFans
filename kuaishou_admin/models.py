import decimal

from django.db import models


# Create your models here.
class Client(models.Model):
    wechat_id = models.CharField(max_length=20, default='')
    # 总消费
    consume_gold = models.IntegerField(default=0)
    # 联系方式
    phone_num = models.IntegerField(default=0)
    # 金币
    gold = models.IntegerField(default=0)
    # 用户名
    name = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.name

    def to_dict(self):
        dict = {
            "user_id": self.wechat_id,
            "user_name": self.name,
            "gold": self.gold,
            "phone_num": self.phone_num,
            "consume_gold": self.consume_gold
        }
        return dict

    class Meta:
        db_table = "kuaishou_client"


class Project(models.Model):
    '''
    项目表
    '''
    pro_name = models.CharField(max_length=100, blank=False)
    count_project = models.IntegerField()
    pro_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))
    combo = models.ManyToManyField('Order_combo', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "kuaishou_project"


class Order(models.Model):
    '''
    订单表
    '''
    choices_status = (
        (0, "未开始"),
        (1, "执行中"),
        (2, "已完成"),
        (3, "异常单"),
        (4, "已撤单"),
    )
    client = models.ForeignKey('Client')
    project = models.ForeignKey('Project')

    gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))
    data = models.TextField(default="")
    create_date = models.DateTimeField(auto_now_add=True)
    showdata = models.TextField(default="")
    count_init = models.IntegerField(default=0)
    type_id = models.IntegerField(default=0)
    kuaishou_id = models.CharField(max_length=20)
    link_works = models.URLField()
    status = models.IntegerField(default=0, choices=choices_status)
    order_id_num = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def to_dict(self):
        order_dict = {
            "order_id": self.order_id_num,
            "project_name": self.project.pro_name,
            "kuaishou_id": self.kuaishou_id,
            "ordered_num": self.count_init,
            "status_order": self.status,
            "production_link": self.link_works,
            "user_name": self.client.name,
            "create_order_time": self.create_date
        }
        return order_dict

    class Meta:
        db_table = "kuaishou_order"


class Order_combo(models.Model):
    '''
    套餐表
    '''
    name = models.CharField(max_length=100, null=False)
    detail_combo = models.ManyToManyField('Project', blank=True)
    pro_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "kuaishou_combo"


class Old_Order_project(models.Model):
    '''
    扩展表  历史记录表
    '''
    old_gold = models.DecimalField("积分", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))

    orders = models.OneToOneField('Order', null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "kuaishou_expend_ord"
