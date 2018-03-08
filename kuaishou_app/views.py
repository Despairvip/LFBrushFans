import json
import logging
import os
import random
import re

from alipay import AliPay
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
from django.views.generic import View
from kuaishou_admin.models import Project, Client, Order
from utils.views import createOrdernumber as create_num, gifshow,Create_alipay_order as create_alipay
from hashids import Hashids



# 实例化一个无水印下载对象
down = gifshow()
# 实例化一个加密对象
q = Hashids()
# 实例化一个日志对象
logger_db = logging.getLogger("db")


class ClickView(View):
    def post(self, request):
        pass


class PlayView(View):
    def post(self, request):
        pass


class FansView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        hands_id = data.get("hands_id")
        fan_num = data.get("fan_num")
        gold = int(data.get("gold"))
        wechat_id = data.get('wechat_id')
        user = Client.objects.filter(wechat_id=wechat_id).first()
        pro = Project.objects.filter(pro_name="刷粉丝").first()

        # 判断用户积分
        user_gold = user.gold
        consume_gold = user.consume_gold
        if user_gold < gold:
            return JsonResponse(data={"msg": "积分不够"})
        if consume_gold < 0:
            return JsonResponse(data={"msg": "用户积分为负数"})

        # 生成订单编号
        order_id_num = create_num(wechat_id, pro.id)
        # 创建订单
        try:
            order = Order()
            order.client = user
            order.project = pro
            order.gold = gold
            order.count_init = fan_num
            order.type_id = 0
            order.kuaishou_id = hands_id
            order.order_id_num = order_id_num

            order.save()

            user.consume_gold += gold
            user.gold -= gold
            user.save()
        except Exception as e:
            user.consume_gold = consume_gold
            user.gold = gold
            user.save()
            return JsonResponse(data={'msg': print(e)})

        user.save()
        hs_order_id_num = q.encode(int(order_id_num))
        return JsonResponse(data={'order_num': hs_order_id_num})


class IntegralView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        order_id = data.get('gold')
        gold = data.get('gold')






class CenterView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        wechat_id = data.get('wechat_id')
        try:
            user = Client.objects.filter(wechat_id=wechat_id).first()
        except Exception as e:
            return JsonResponse(data={'msg': "没有查到用户信息"})
        content = {
            "avatar": user.avatar,
            "user_name": user.name,
            "hands_id": user.wechat_id,
            "gold": user.gold
        }
        return JsonResponse(data=content)


class ConfirmView(View):
    def post(self):
        pass


class DownloadView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        works = data.get("works")
        # 提取photo_id
        try:
            photoId = re.search(r'photoId=(\d+)', works).group(1)
        except Exception as e:
            return JsonResponse(data={"msg":"格式错误"})
        print(photoId.encode())
        hs_link = down.photo_info(photoId)
        print(type(hs_link))
        print(hs_link)
        link = hs_link["photos"][0]["main_mv_urls"][0]["url"]
        return JsonResponse(data={'link':link})


class NotesView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        wechat_id = data.get("wechat_id")
        try:
            orders = Order.objects.filter(client__wechat_id__exact=wechat_id).all()
        except Exception as e:

            return JsonResponse(data={'msg': print(e)})
        content = []
        if orders:
            for order in orders:
                content.append({
                    "pro_name": order.project.pro_name,
                    "pro_gold": order.gold,
                    "pro_num": order.count_init,
                    "time": order.create_date
                })
        else:
            return JsonResponse(data={"用户没有订单"})
        return JsonResponse(data={'msg': content})


class NewsView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        hands_id = data.get("hands_id")
        wechat_id = data.get("wechat_id")
        try:
            user = Client.objects.filter(wechat_id=wechat_id)
        except Exception as e:
            logger_db.error(e)
            return JsonResponse(data={"msg": "wechat_id 错误"})
        if user:
            try:
                user.update(hands_id=hands_id)
            except Exception as e:
                logger_db.error(e)
                return JsonResponse(data={"msg": "False"})
        return JsonResponse(data={"msg": "True"})


class Alipay(View):
    def post(self,request):
        data = json.loads(request.body.decode())
        wechat_id = data.get("wechat_id")
        money = data .get("gold")
        alipay = create_alipay()
        # App支付，将order_string返回给app即可
        order_id = create_num(wechat_id,1)
        order_string = alipay.api_alipay_trade_app_pay(
            out_trade_no=order_id,
            total_amount=money,
            subject="LFBrushFans%s" % order_id,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        hs_order_id = q.decode(order_id)
        return JsonResponse(data={"ali_msg": order_string,"order_id":hs_order_id})







class CheckPayStatusView(View):
    def post(self,request):
        order_id = q.decode(json.loads(request.body.decode()))[0]

        try:
            order = Order.objects.filter(order_id_num=order_id).first()
        except Exception as e:

            return JsonResponse(data={"msg":"获取订单失败"})
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, "kuaishou_app/app_private_key.pem"),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, "kuaishou_app/alipay_public_key.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False  配合沙箱模式使用
        )
        while True:
            response = alipay.api_alipay_trade_query(order_id)

            code = response.get("code")
            trade_status = response.get("trade_status")

            if code == "10000" and trade_status == "TRADE_SUCCESS":
                pass


class abc(View):
    def get(self,request):
        return JsonResponse(data={"msg":"111"})