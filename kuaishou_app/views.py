import json
import logging
import random
import re
from distutils.version import LooseVersion

import redis
import requests
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from backManage.core import userid_to_secret, create_token, secret_to_userid
from common.returnMessage import MessageResponse
from sfpt import settings

from django.core.paginator import Paginator
from django.http import JsonResponse
from hashids import Hashids

from kuaishou_admin.models import Project, Client, Order, Order_combo, CheckVersion, AdminManagement, MoneyAndGold, \
    LoginFrom, Combo_project
from kuaishou_app.models import PayListModel
from utils.tornado_websocket.lib_redis import RedisHelper
from utils.views import createOrdernumber as create_num, gifshow, Create_alipay_order as create_alipay, \
    socket_create_order_time, Create_wechatpay_order as create_wechat, \
    conditions, expired_message, check_token

expired_message()
down = gifshow()
# 实例化一个加密对象
q = Hashids()
# 实例化一个日志对象
logger = logging.getLogger("django_app")

conn = redis.Redis()


@check_token
def show_gold_money(request):
    """
    传递金钱和积分给前端
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            moneyAndGold = MoneyAndGold.objects.order_by("money")
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        else:

            data = []
            for detial in moneyAndGold:
                data_dict = {}

                data_dict["money"] = detial.money
                data_dict["gold"] = detial.gold

                data.append(data_dict)

            return MessageResponse(0, data=data)


@check_token
def ClickView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        works_link = data.get('works')


        client_id = data.get("user_id")


        kuaishou_id = data.get('hands_id')
        project_id = data.get('project_id')
        # pro_id = data.get('pro_id') #用户点击的是双击项目里面的哪个具体双击数和积分  // 周周
        token = data.get("token")

        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})
        # 项目金币、数量
        try:
            project = Project.objects.get(id=project_id)

        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" :2001 ,"msg" : "项目不存在"})
        click_num = project.count_project
        need_gold = project.pro_gold

        # 检验用户

        if works_link and project_id and client_id and client_id is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})
        if len(str(client_id)) != 4:
            return JsonResponse(data={"status": 2004})
        try:
            client = Client.objects.filter(id=client_id).first()
            if client is None:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})

        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "用户token错误"})

        project = Project.objects.filter(id=project_id).first()

        if project is None:
            return JsonResponse(data={'status': 5003, 'msg': '项目错误'})
        click_num = project.count_project
        need_gold = project.pro_gold

        # 判断金币余额

        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})

        # ----------------订单操作---------------
        order_id = create_num(client_id, project_id)
        hs_order_id_num = q.encode(int(order_id))
        msg = {
            "status_order": "未开始",
            "ordered_num": click_num,
            "user_name": client_id,
            "work_links": works_link,
            "project_name": project.pro_name,
            "order_id": hs_order_id_num,
            "kuaishou_id": kuaishou_id,
            "create_order_time": socket_create_order_time()
        }
        msg_json = json.dumps(msg)
        obj = RedisHelper()

        obj.public(msg_json)
        order = Order(gold=need_gold, client=client, kuaishou_id=kuaishou_id, link_works=works_link,
                      count_init=click_num, project=project, order_id_num=order_id)
        order.save()
        return JsonResponse(data={'status': 0, "order_num": hs_order_id_num})


@check_token
def PlayView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        works_link = data.get('works')
        # play_num = data.get('play_num')
        # need_gold = data.get('gold')
        project_id = data.get('project_id')

        kuaishou_id = data.get('hands_id')

        token = data.get("token")

        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})

            # 项目金币、数量
        try:
            project = Project.objects.get(id=project_id)

        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 2001, "msg": "项目不存在"})
        play_num = project.count_project
        need_gold = project.pro_gold


        if works_link and project_id and client_id is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})
        if len(str(client_id)) != 4:
            return JsonResponse(data={"status": 2004})
        try:
            client = Client.objects.filter(id=client_id).first()
            if not client:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})
        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "token验证失败"})
        project = Project.objects.filter(id=project_id).first()
        if project is None:
            return JsonResponse(data={'status': 5003, 'msg': '项目错误'})

        play_num = project.count_project
        need_gold = project.pro_gold
        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})

        # -----------订单处理-------------------
        order_id = create_num(client_id, project_id)
        hs_order_id_num = q.encode(int(order_id))
        msg = {
            "status_order": "未开始",
            "ordered_num": play_num,
            "user_name": client_id,
            "work_links": works_link,
            "project_name": project.pro_name,
            "order_id": hs_order_id_num,
            "kuaishou_id": kuaishou_id,
            "create_order_time": socket_create_order_time(),
        }
        msg_json = json.dumps(msg)
        obj = RedisHelper()
        obj.public(msg_json)

        order = Order(order_id_num=order_id, gold=need_gold, project=project, client=client, count_init=play_num,
                      link_works=works_link, kuaishou_id=kuaishou_id)
        order.save()

        return JsonResponse(data={'status': 0, "order_id": hs_order_id_num})


@check_token
def FansView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        hands_id = data.get("hands_id")
        # fan_num = data.get("fan_num")
        # need_gold = int(data.get("gold"))
        project_id = data.get("project_id")
        token = data.get("token")
        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})

        # 判断金币
            # 项目金币、数量
        try:
            project = Project.objects.get(id=project_id)

        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 2001, "msg": "项目不存在"})
        fan_num = project.count_project
        need_gold = project.pro_gold


        if hands_id and client_id and hands_id is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        if len(str(client_id)) != 4:
            return JsonResponse(data={"status": 2004})
        try:
            client = Client.objects.filter(id=client_id).first()
            if client is None:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
            if client.token != token:
                return JsonResponse(data={"status": 5003, "msg": "token验证不通过"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})
        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "token错误"})

        project = Project.objects.filter(id=project_id).first()

        if project is None:
            return JsonResponse(data={'status': 5003, 'msg': '项目错误'})

        fan_num = project.count_project
        need_gold = project.pro_gold

        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})

        order_id = create_num(client_id, project_id)
        hs_order_id_num = q.encode(int(order_id))
        msg = {
            "status_order": "未开始",
            "ordered_num": fan_num,
            "user_name": client_id,
            "work_links": None,
            "project_name": project.pro_name,
            "order_id": hs_order_id_num,
            "kuaishou_id": hands_id,
            "create_order_time": socket_create_order_time(),
        }
        msg_json = json.dumps(msg)
        obj = RedisHelper()
        obj.public(msg_json)
        # 创建订单
        try:
            order = Order()
            order.client = client
            order.project = project
            order.gold = need_gold
            order.count_init = fan_num
            order.type_id = 0
            order.kuaishou_id = hands_id
            order.order_id_num = order_id

            order.save()

        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, 'msg': print(e)})

        return JsonResponse(data={'status': 0, 'order_num': hs_order_id_num})


@check_token
def ConfirmView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        package_id = data.get('package_id')
        # need_gold = data.get('gold')
        works_link = data.get('works')
        kuaishou_id = data.get('hands_id')

        token = data.get("token")

        if package_id and works_link and kuaishou_id is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})



        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})

        # 判断金币
        try:
            combo = Order_combo.objects.get(id=package_id)

        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 2004,"msg" : "套餐不存在"})
        need_gold = combo.pro_gold

        # 判断用户信息
        if package_id and need_gold and works_link and kuaishou_id and client_id is None:

            return JsonResponse(data={"status": 3103, "msg": "参数不全"})
        if len(str(client_id)) != 4:
            return JsonResponse(data={"status": 2004})
        try:
            client = Client.objects.filter(id=client_id).first()
            if client is None:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})
        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "用户token"})

        order_combo = Order_combo.objects.filter(id=package_id).first()
        need_gold = order_combo.pro_gold
        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})

        order_id = create_num(client_id, 100)
        hs_order_id = q.encode(int(order_id))
        # ------------订单处理--------------------




        msg = {
            "status_order": "未开始",
            "ordered_num": '',
            "user_name": client_id,
            "work_links": works_link,
            "project_name": order_combo.name,
            "order_id": hs_order_id,
            "kuaishou_id": kuaishou_id,
            "create_order_time": socket_create_order_time(),
        }
        msg_json = json.dumps(msg)
        obj = RedisHelper()
        obj.public(msg_json)
        order = Order(gold=need_gold, combo=order_combo, client=client, kuaishou_id=kuaishou_id,
                      link_works=works_link, order_id_num=order_id, count_init=0, type_id=1)

        order.save()

        return JsonResponse({'status': 0, 'order_num': hs_order_id})


@check_token
def IntegralView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        order_id = q.decode(data.get('order_id'))[0]
        gold = data.get('gold')
        pay_type = data.get("pay_type")
        token = data.get("token")

        # 校验数据

        if order_id and gold and pay_type is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})

        try:
            client = Client.objects.filter(id=client_id).first()
            pay = PayListModel.objects.filter(order_id=order_id).first()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={'status': 4001, "msg": print(e)})
        if client or pay is None:
            return JsonResponse(data={'status': 4003, 'msg': "id或订单号出问题"})

        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "用户token"})

        # 支付宝支付

        if pay_type == 0 or pay_type == 1:
            try:
                pay_order = PayListModel.objects.filter(order_id=order_id).firest()
            except Exception as e:
                logger.error(e)
                return JsonResponse(data={"status" :2001 ,"msg" :"数据获取错误"})
            if pay_order is None:
                return JsonResponse(data={"status" : 2004,"msg" : "订单不存在"})
            if pay_order.status == 1:
                db_gold = MoneyAndGold.objects.filter(money=pay_order.money).first()
                gold = db_gold.gold
                try:
                    pay_order.client.gold += gold
                    pay_order.save()
                except Exception as e:
                    logger.error(e)
                    return JsonResponse(data={"status" : 2001,"msg" : "积分修改失败"})
                return JsonResponse(data={"status" : 0,"msg" : "充值成功"})





        # elif pay_type == 1:
        #     try:
        #         pay_order = PayListModel.objects.filter(order_id=order_id).firest()
        #     except Exception as e:
        #         logger.error(e)
        #         return JsonResponse(data={"status" :2001 ,"msg" :"数据获取错误"})
        #     if pay_order is None:
        #         return JsonResponse(data={"status" : 2004,"msg" : "订单不存在"})
        #     if pay_order.status == 1:
        #         db_gold = MoneyAndGold.objects.filter(money=pay_order.money).first()
        #         gold = db_gold.gold
        #         try:
        #             pay_order.client.gold += gold
        #             pay_order.save()
        #         except Exception as e:
        #             logger.error(e)
        #             return JsonResponse(data={"status" : 2001,"msg" : "积分修改失败"})
        #         return JsonResponse(data={"status" : 0,"msg" : "充值成功"})



''' written by Despair
    支付回调函数
'''


@csrf_exempt
def notify(request,pay_type):
    data = request.POST.dict()

    if pay_type == "alipay":
        # 签名认证 返回结果给支付宝
        signature = data.pop("sign")
        print(signature)
        alipay = create_alipay()
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            # 订单号
            out_trade_no = request.POST.get("out_trade_no")
            # 流水号
            trade_no = request.POST.get("trade_no")
            # 用户支付的金额
            total_amount = request.POST.get("total_amount")

            money_order = PayListModel.objects.filter(ddh=out_trade_no).first()
            # 修改状态
            if money_order is None:
                return JsonResponse(data={"status" :2004 ,"msg" :"订单不存在"})
            if money_order.money != total_amount:
                return JsonResponse(data={"status" : 2002,"msg" :"支付金额出错"})
            money_order.Amount_money = total_amount
            money_order.status = 1
            money_order.trade_no = trade_no
            money_order.save()

            print("trade succeed")
            return HttpResponse("success")

    elif pay_type =="wechat":
        xml = request.body.decode()["xml"]
        print(xml)
        wechat = create_wechat()
        data = wechat.parse_payment_result(xml)
        if data["return_code"] == "SUCCESS":
            # 自己的订单号
            my_order_id = data["out_trade_no"]
            money_order = PayListModel.objects.filter(order_id=my_order_id).first()
            # 用户支付金额
            user_money = data["cash_fee"]
            # 平台订单号
            wechat_pay_id = data["transaction_id"]


            money_order.Amount_money = user_money
            money_order.status = 1
            # 微信支付平台订单号
            money_order.trade_no = wechat_pay_id
            money_order.save()

            return JsonResponse(data={"return_code" :"SUCCESS" ,"return_msg" :"OK"})
        else:

            return JsonResponse(data={"return_code" :"error" ,"return_msg" :"-1"})


'''
xialing:alipay，qq登陆,wechat登陆
zhouzhou:wechatpay,wechat登陆


'''


@check_token
def PayApi(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        gold = data.get("gold")
        money = data.get("money")
        pay_type = data.get("pay_type")

        # 金钱检测
        db_gold = MoneyAndGold.objects.values_list("gold","money")

        if (gold,money) not in db_gold:
            return JsonResponse(data={"status" : 2004,"msg" : "金币有误"})

        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})
        # 用户校验
        if client_id and money and pay_type is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        # 开启支付
        client = Client.objects.get(id=client_id)
        order_id = create_num(client_id, 1)
        try:
            if pay_type == 0:
                ali_pay = create_alipay()
                # App支付，将order_string返回给app即可

                # 创建支付宝支付数据
                pay_num, order_string = ali_pay.api_alipay_trade_app_pay(
                    out_trade_no=order_id,
                    total_amount=money,
                    subject="LFBrushFans%s" % order_id,

                    # 添加回调地址
                    notify_url= "sfpt.remenhezi.com/pay/new/notify/alipay"  # 可选, 不填则使用默认notify url
                )
                # print(pay_num)
                # 创建支付订单
                pay_order = PayListModel()
                pay_order.order_id = order_id
                pay_order.client = client
                pay_order.money = money
                pay_order.order_type = pay_type
                pay_order.ddh = pay_num

                pay_order.save()

                hs_order_id = q.encode(int(order_id))
                return JsonResponse(data={"status": 0, "ali_msg": order_string, "order_id": hs_order_id})

            elif pay_type == 1:
                wechat_pay = create_wechat()
                # 统一支付接口
                result = wechat_pay.order.create(
                    out_trade_no=order_id,
                    trade_type='App',
                    body="LFBrushFans%s" % order_id,
                    total_fee=money,

                    # 添加回调地址
                    notify_url= "sfpt.remenhezi.com/pay/new/notify/wechat"
                )

                payment = wechat_pay.order.get_appapi_params(result["prepay_id"])

                # 保存交易信息
                pay_order = PayListModel()
                pay_order.order_id = order_id

                pay_order.client.id = client_id
                pay_order.money = money
                pay_order.order_type = pay_type

                pay_order.save()

                hs_order_id = q.encode(int(order_id))
                return JsonResponse(data={"status": 0, "wechat_msg": payment, "order_id": hs_order_id})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"status": 3001, 'msg': "异常重新尝试"})


'''

xialing
'''


@check_token
def CenterView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})

        if client_id is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        try:
            user = Client.objects.filter(id=client_id).first()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 5003, 'msg': "没有查到用户信息"})
        if user is None:
            return JsonResponse(data={"status": 5002, "msg": "用户id错误"})
        content = user.to_dict()
        print(content)
        return JsonResponse(data={"status": 0, "data": content})


'''

xialing
'''


@check_token
def DownloadView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        works = data.get("works")
        if works is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        # 提取photo_id
        try:
            photoId = re.search(r'photoId=(\d+)', works).group(1)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4003, "msg": "格式错误"})

        hs_link = down.photo_info(photoId)

        link = hs_link["photos"][0]["main_mv_urls"][0]["url"]
        return JsonResponse(data={"status": 0, 'link': link})


'''
xialing

'''


@check_token
def NotesView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        # 序列化用户id
        if data.get("user_id") is None:
            return JsonResponse(data={"status": 2004, "msg": "参数不全"})
        try:
            client_id = secret_to_userid(data.get("user_id"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status" : 3104,"msg" : "用户不存在"})


        page = data.get("page", 1)
        # 一页几条数据
        num_page = data.get("num_page", 10)
        if client_id is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        try:
            orders = Order.objects.filter(client__id__exact=client_id).all().order_by("-create_date")
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, 'msg': print(e)})
        content = []
        if orders:
            for order in orders:
                result = {
                    "pro_gold": order.gold,
                    "pro_num": order.count_init,
                    "time": order.create_date,
                }
                if order.project is None:
                    result['pro_name'] = order.combo.name
                else:
                    result["pro_num"] = order.project.pro_name
                content.append(result)
        else:
            return JsonResponse(data={"status": 5003, "msg": "用户没有订单"})
        p = Paginator(content, num_page)
        count = p.count
        if int(page) > int(count):
            return JsonResponse("")
        pages = p.num_pages
        pages_ss = p.page(page).object_list
        return JsonResponse(data={"status": 0, "data": pages_ss, "count": count, "pages": pages})


'''
xialing and zhouzhou

'''


def ClientLoginView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        type = data.get('type')
        if type is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})

        elif type == '0':
            code = data['code']
            secret = settings.SECRET_APP
            appid = 'wx5f4ea0928a45436d'
            if code is not None:
                res = requests.get(
                    'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
                        appid, secret, code))
            else:
                return JsonResponse(data={"status": 4003, "msg": 'code错误'})

            res_dict = res.json()
            if res_dict.get('errcode') is not None:
                return JsonResponse(data={"status": 4003, "msg": res_dict.get("errcode")})
            res_data_openid = res_dict['openid']
            token = res_dict['access_token']

            user_info = requests.get('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s' % (
                token, res_data_openid)).json()
            client_name = user_info['nickname'].encode('iso-8859-1').decode('utf-8')
            avatar_url = user_info['headimgurl']
            unionid = user_info["unionid"]

            if user_info.get('errcode') is not None:
                return JsonResponse(data={"status": 6000, "msg": user_info.get("errcode")})

            # 处理用户

            client = Client.objects.filter(unionid=unionid).first()
            if client is not None:
                client.token = token
                client.avatar = avatar_url
                client.nickname = client_name
                client.save()
                return JsonResponse(data={"status": 0, "data": client.to_dict(), "token": token})

            client = Client(username=res_data_openid, nickname=client_name, avatar=avatar_url, token=token, unionid=unionid,
                            )
            client.save()
            # 第三方登录信息
            third_from = LoginFrom()
            third_from.client = client
            third_from.third_name = "wechat"
            third_from.app_id = appid
            third_from.openid = res_data_openid
            ###
            content = client.to_dict()
            user_id = content["user_id"]

            # //
            # 添加token
            my_token = create_token(user_id)

            return JsonResponse(data={"status": 0, "data": content, "token": my_token})
        # qq登陆
        elif type == "1":
            openid = data.get('openid')
            oauth_consumer_key = data.get('oauth_consumer_key')
            token = data.get("access_token")
            res = requests.get(
                'https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s' % (
                    token, oauth_consumer_key, openid)).json()

            avatar = res.get("figureurl_2")

            nickname = res.get("nickname")

            # 处理用户

            client = Client.objects.filter(unionid=openid).first()
            if client is not None:
                client.avatar = avatar

                client.nickname = nickname
                client.save()
                return JsonResponse(data={"status": 0, "data": client.to_dict(), "token": token})
            try:
                client = Client(username=openid, nickname=nickname, avatar=avatar, unionid=openid,
                                token=token)
                client.save()

                # 设置第三方登录信息
                third_from = LoginFrom()
                third_from.client = client
                third_from.third_name = 'qq'
                third_from.app_id = 'null'
                third_from.openid = openid
                third_from.save()

            except Exception as e:
                return JsonResponse({"msg": print(e)})

            content = client.to_dict()
            user_id = content["user_id"]

            # 添加token
            my_token = create_token(user_id)
            print(my_token)
            return JsonResponse(data={"status": 0, 'data': content, "token": my_token})
        else:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})


"""written by Despair"""


def check_update(request):
    '''检查更新'''
    data = json.loads(request.body.decode())
    version_code = data.get("version_code")
    client_version = LooseVersion(str(version_code))
    # if version_code is None:
    #     return HttpResponseRedirect("http://yuweining.cn/t/Html5/404html/")

    try:
        # 获取最新版本号
        version_query = CheckVersion.objects
        version_set = version_query.first()
        version = version_set.version

    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status": 4001, "msg": "获取失败"})

    new_version = LooseVersion(str(version))
    sdk_url = version_set.sdk_url
    update_msg = version_set.update_msg

    content = {
        "version": version,
        "sdk_url": sdk_url,
        "update_msg": update_msg
    }

    # if client_version is None:
    #     return JsonResponse(data={"status": 0, "data": content})

    if version_code is None:
        return JsonResponse(data={"status": 4002, "data": content})

        # 进行对比
    if new_version > client_version:
        return JsonResponse(data={"status": 4203, "data": content})

    return JsonResponse(data={"status": 0, "msg": "不用更新"})


"""written by Despair"""


def admin_id(request):
    '''客服微信号列表'''

    try:
        admin_ids = AdminManagement.objects.all()
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
    if admin_ids is None:
        return JsonResponse(data={"status": 4001, "msg": "没有数据"})
    content = []
    for admin in admin_ids:
        content.append(admin.wechat)
    return JsonResponse(data={"status": 0, "data": content})


"""written by Despair"""


def shield_wechat(request):
    '''written by Despair
     屏蔽微信登陸
     '''
    return JsonResponse(data={"data": False})
