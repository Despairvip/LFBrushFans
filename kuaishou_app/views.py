import json
import logging
import re

import redis
import requests
from Demo import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from hashids import Hashids

from kuaishou_admin.models import Project, Client, Order, Order_combo
from kuaishou_app.models import PayListModel
from utils.tornado_websocket.lib_redis import RedisHelper
from utils.views import createOrdernumber as create_num, gifshow, Create_alipay_order as create_alipay, \
    socket_create_order_time, handle_user_id, Create_wechatpay_order as create_wechat, \
    conditions, expired_message, check_token

down = gifshow()
# 实例化一个加密对象
q = Hashids()
# 实例化一个日志对象
logger = logging.getLogger("django_app")

conn = redis.Redis()


@check_token
def ClickView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        works_link = data.get('works')
        click_num = data.get('click_num')
        need_gold = data.get('gold')
        client_id = data.get("user_id")
        print(client_id)
        wechat_id = handle_user_id(data.get('user_id'))
        kuaishou_id = data.get('hands_id')
        project_id = data.get('project_id')
        token = data.get("token")

        try:
            client = Client.objects.filter(id=wechat_id).first()
            if client is None:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})
        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "用户token"})

        project = Project.objects.filter(id=project_id).first()

        if project is None:
            return JsonResponse(data={'status': 5003, 'msg': '项目错误'})

        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})





        # ----------------订单操作---------------
        order_id = create_num(wechat_id, project_id)
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
        works_link = data['works']
        play_num = data['play_num']
        need_gold = data['gold']
        project_id = data['project_id']
        client_id = data.get("user_id")
        user_id = handle_user_id(data.get('user_id'))
        kuaishou_id = data['hands_id']

        token = data.get("token")

        try:
            client = Client.objects.filter(id=user_id).first()
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

        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})


        # -----------订单处理-------------------
        order_id = create_num(user_id, project_id)
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
        fan_num = data.get("fan_num")
        need_gold = int(data.get("gold"))
        wechat_id = handle_user_id(data.get('user_id'))
        project_id = data.get("project_id")
        client_id = data.get("user_id")
        token = data.get("token")

        try:
            client = Client.objects.filter(id=wechat_id).first()
            if client is None:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
            if client.token != token:
                print(client.token)
                return JsonResponse(data={"status": 5003, "msg": "token验证不通过"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})
        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "token错误"})

        project = Project.objects.filter(id=project_id).first()

        if project is None:
            return JsonResponse(data={'status': 5003, 'msg': '项目错误'})

        if not conditions(client, need_gold):
            print(need_gold)
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})

        order_id = create_num(wechat_id, project_id)
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
        package_id = data['package_id']
        need_gold = data['gold']
        user_id = handle_user_id(data.get('user_id'))
        works_link = data['works']
        kuaishou_id = data['hands_id']
        client_id = data.get("user_id")

        token = data.get("token")

        try:
            client = Client.objects.filter(id=user_id).first()
            if client is None:
                return JsonResponse(data={"status": 5001, "msg": "用户未登录"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": print(e)})
        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "用户token"})

        if not conditions(client, need_gold):
            return JsonResponse(data={'status': 5005, 'msg': '积分不足'})

        order_id = create_num(user_id, 100)
        hs_order_id = q.encode(int(order_id))
        # ------------订单处理--------------------
        if package_id in [1, 2, 3, 4, 5, 6]:
            order_combo = Order_combo.objects.filter(id=package_id).first()

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
                          link_works=works_link, count_init=0, type_id=1)

            order.save()
        else:
            return JsonResponse({'status': 4003, 'msg': '套餐不存在'})
        return JsonResponse({'status': 0, 'order_num': hs_order_id})


@check_token
def IntegralView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        order_id = q.decode(data.get('order_id'))[0]
        gold = data.get('gold')
        pay_type = data.get("pay_type")
        user_id = handle_user_id(data.get("user_id"))
        token = data.get("token")
        try:
            client = Client.objects.filter(id=user_id).first()
            pay = PayListModel.objects.filter(order_id=order_id).first()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={'status': 4001, "msg": print(e)})
        if client or pay is None:
            return JsonResponse(data={'status': 4003, 'msg': "id或订单号出问题"})

        if client.token != token:
            return JsonResponse(data={"status": 5003, "msg": "用户token"})
        if pay_type == '0':
            alipay = create_alipay()
            while True:
                response = alipay.api_alipay_trade_query(order_id)  # response是一个字典

                # 判断支付结果
                code = response.get("code")  # 支付宝接口调用成功或者错误的标志
                trade_status = response.get("trade_status")  # 用户支付的情况

                if code == "10000" and trade_status == "TRADE_SUCCESS":
                    # 表示用户支付成功
                    # 修改订单的状态，变为待评论状态
                    pay.status = 0
                    # 更新订单的支付宝交易编号
                    pay.ddh = response.get("trade_no")
                    pay.save()
                    client.gold += gold
                    client.save()
                    return JsonResponse({"code": 0, "message": "支付成功"})
                elif code == "40004" or code == "10000":
                    # 表示支付宝接口调用暂时失败，（支付宝的支付订单还未生成） 后者 等待用户支付
                    # 继续查询
                    continue
                else:
                    # 支付失败
                    # 返回支付失败的通知
                    return JsonResponse({"code": 3001, "msg": "支付失败"})
        elif pay_type == 1:
            wechat_pay = create_wechat()
            while True:
                result = wechat_pay.order.query(out_trade_no=order_id)
                return_code = result.get("return_code")
                result_code = result.get('result_code')
                if return_code == "SUCCESS":
                    return JsonResponse({"status": 3001, "msg": result.get("return_msg")})
                if return_code == "SUCCESS" and result_code == "SUCCESS":
                    pay.status = 0
                    pay.ddh = result.get("transaction_id")
                    pay.save()
                    client.gold += gold
                    client.save()
                    return JsonResponse({"code": 0, "msg": "支付成功"})

'''
xialing:alipay，qq登陆,wechat登陆
zhouzhou:wechatpay,wechat登陆


'''
@check_token
def PayApi(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        user_id = handle_user_id(data.get('user_id'))
        money = data.get("money")
        pay_type = data.get("pay_type")
        order_id = create_num(user_id, 1)
        try:
            if pay_type == '0':
                ali_pay = create_alipay()
                # App支付，将order_string返回给app即可


                order_string = ali_pay.api_alipay_trade_app_pay(
                    out_trade_no=order_id,
                    total_amount=money,
                    subject="LFBrushFans%s" % order_id,
                    notify_url='http://120.26.60.181:8001/pay/new/notify/alipay'  # 可选, 不填则使用默认notify url
                )
                print(order_id)
                hs_order_id = q.encode(int(order_id))
                return JsonResponse(data={"status": 0, "ali_msg": order_string, "order_id": hs_order_id})
            wechat_pay = create_wechat()
            # 统一支付接口
            result = wechat_pay.order.create(
                out_trade_no=order_id,
                trade_type='App',
                body="LFBrushFans%s" % order_id,
                total_fee=money,
                notify_url='http://192.168.0.159:4444/#/home'
            )

            payment = wechat_pay.order.get_appapi_params(result["prepay_id"])
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
        user_id = handle_user_id(data.get('user_id'))
        try:
            user = Client.objects.filter(id=user_id).first()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 5003, 'msg': "没有查到用户信息"})
        content = user.to_dict()
        return JsonResponse(data={"status": 0,"data":content})

'''

xialing
'''
@check_token
def DownloadView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        works = data.get("works")
        # 提取photo_id
        try:
            photoId = re.search(r'photoId=(\d+)', works).group(1)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4003, "msg": "格式错误"})
        print(photoId.encode())
        hs_link = down.photo_info(photoId)
        print(type(hs_link))
        print(hs_link)
        link = hs_link["photos"][0]["main_mv_urls"][0]["url"]
        return JsonResponse(data={"status": 0, 'link': link})

'''
xialing

'''
@check_token
def NotesView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        user_id = handle_user_id(data.get('user_id'))
        page = data.get("page", 1)
        # 一页几条数据
        num_page = data.get("num_page", 10)
        try:
            orders = Order.objects.filter(client__id__exact=user_id).all()
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
        if page > count:
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

        type = data['type']
        if type == '0':
            code = data['code']
            secret = settings.SECRET_APP
            appid = settings.APP_ID
            if code is not None:
                res = requests.get(
                    'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
                        appid, secret, code))
            else:
                return JsonResponse(data={"status": 4003, "msg": 'code错误'})
            print(res)
            res_dict = res.json()
            if res_dict.get('errcode') is not None:
                return JsonResponse(data={"status": 4003, "msg": res_dict.get("errcode")})
            res_data_openid = res_dict['openid']
            token = res_dict['access_token']
            print(token)
            user_info = requests.get('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s' % (
                token, res_data_openid)).json()

            client_name = user_info['nickname'].encode('iso-8859-1').decode('utf-8')
            avatar_url = user_info['headimgurl']
            unionid = user_info["unionid"]
            if user_info.get('errcode') is not None:
                return JsonResponse(data={"status": 6000, "msg": user_info.get("errcode")})

            client = Client.objects.filter(unionid=unionid).first()
            if client is not None:
                client.token = token
                client.save()
                return JsonResponse(data={"status": 0, "data": client.to_dict(), "token": token})
            client = Client()
            client.username = client_name
            client.avatar = avatar_url
            client.token = token
            client.unionid = unionid
            client.save()
            content = client.to_dict()
            ###
            conn.set('token:%s' % token, '1')

            return JsonResponse(data={"status": 0, "data": content, "token": token})
        # qq登陆

        openid = data.get('openid')
        oauth_consumer_key = data.get('oauth_consumer_key')
        token = data.get("access_token")
        res = requests.get('https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s' % (
        token, oauth_consumer_key, openid)).json()

        avatar = res.get("figureurl_qq_1")
        nickname = res.get("nickname")
        client = Client.objects.filter(unionid=openid).first()
        if client is not None:
            client.token = token
            client.save()
            return JsonResponse(data={"status":0,"data":client.to_dict(),"token":token})
        try:
            client = Client(username=nickname,avatar=avatar,unionid=openid,login_type=1,token=token)
            client.save()
        except Exception as e:
            return JsonResponse({"msg":print(e)})
        content = client.to_dict()
        print(content)
        return JsonResponse(data={"status":0,'data':content,"token":token})






