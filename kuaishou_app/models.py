import decimal
from django.db import models
from kuaishou_admin.models import Client


class PayListModel(models.Model):
    choices_ordertype = (
        (0,'积分充值'),
        (1,'开通会员'),


    )
    choices_pay_type = (
        (0,"支付宝支付"),
        (1,"微信支付"),
    )

    order_id = models.CharField("订单号",max_length=200)
    ddh = models.CharField("支付平台订单号",max_length=100,default="")
    client = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
    money = models.DecimalField("支付金额", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))   # 理应收钱
    pay_list_date = models.DateTimeField(auto_now_add=True)
    order_type = models.IntegerField("订单类型",choices=choices_ordertype,default=0)
    Amount_money = models.DecimalField("支付金额", max_digits=19, decimal_places=10, default=decimal.Decimal('0.0'))  # 实际收钱
    trade_no = models.CharField("支付宝流水号",max_length=200,default="")

    pay_type = models.IntegerField("支付类型",choices=choices_pay_type,default=1)
    remark = models.TextField("说明",default="")
    status = models.IntegerField("订单状态",choices=(
        (1,"成功"),
        (2,"失败"),
        (3,"等待付款")
    ),default=3)



