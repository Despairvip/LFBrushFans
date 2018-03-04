from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from hashids import Hashids
from kuaishou_admin.models import Order, Client
import json

# Create your views here.

encrypt = Hashids()


class LoginView(View):
    '''登陆'''

    def post(self, request):
        data = json.loads(request.body.decode())
        user_name = data["user_name"]
        password = data["pwd"]
        # 认证用户
        user = authenticate(username=user_name, password=password)
        if user is None:
            return JsonResponse(data={"msg": " user or id error"})

        # 保存用户登陆session信息
        login(request, user)
        # 跳转到主页
        return JsonResponse(data={"msg": 'login success'})


class LogoutView(View):
    '''退出'''

    def post(self, request):
        logout(request)
        return JsonResponse(data={"msg": "logout success"})


class RealOrdersView(View):
    '''实时订单查询'''

    def post(self, request):
        '''实时订单，返回30条数据'''

        return HttpResponse("订单查询成功")


class OptionSearchView(View):
    '''下拉框搜索'''

    def post(self, request):
        # 获取查询订单的类型(默认是所有订单类型)
        data = json.loads(request.body.decode())
        detail_pro = data['detail_pro']
        order_type = data['order_type']

        if detail_pro == "所有项目":

            orders = Order.objects.filter(status=order_type).all()

        else:
            orders = Order.objects.filter(project__pro_name__exact=detail_pro, status=order_type).all()

        result = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = content['ordered_num']
                # 把这个id加密
                hash_order_id = encrypt.encode(order_id)
                content['ordered_num'] = hash_order_id
                result.append(content)

        return JsonResponse(data={"msg": result})


class EnterSearchView(View):
    '''输入框搜索 order'''

    def post(self, request):
        data = json.loads(request.body.decode())
        if "kuaishou_id" in data:
            kuaishou_id = data['kuaishou_id']
            orders = Order.objects.filter(kuaishou_id=kuaishou_id).all()
        else:
            hs_order_id = data["order_id"]
            order_id = encrypt.decode(hs_order_id)[0]
            print(order_id)
            orders = Order.objects.filter(order_id_num=order_id).all()

        message = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = content['ordered_num']
                hs_order_id = encrypt.encode(order_id)
                content['ordered_num'] = hs_order_id
                message.append(content)
        else:
            return JsonResponse(data={"msg": "wrong format"})

        return JsonResponse(data={'msg': message})


class UserSearchView(View):
    '''用户名字/id 搜索'''

    def post(self, request):
        '''搜索功能'''
        user_id = request.POST.get("user_id", None)
        user_name = request.POST.get("user_name")

        if user_id is not None:
            orders = Order.objects.filter(client__wechat_id__exact=user_id).all()
        else:
            orders = Order.objects.filter(client__name__exact=user_name).all()

        result = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = order.order_id_num
                # 把这个id加密
                hash_order_id = encrypt.encode(order_id)
                content['user_id'] = hash_order_id
                result.append(content)

        return JsonResponse(data={"msg": result})


class ModifyStatusView(View):
    '''修改订单状态'''

    def post(self, request):
        data = json.loads(request.body.decode())

        order_status = data["order_status"]
        hs_order_id = data['order_id']
        order_id = encrypt.decode(hs_order_id)[0]

        order = Order.objects.filter(order_id_num=order_id).update(status=order_status)
        if not order:
            return JsonResponse(data={"result":True})
        return JsonResponse({'result': True})


class ModifyGoldView(View):
    '''修改金币'''

    def post(self, request):
        # 获取用户的id,和需要修改的金币数
        data = json.loads(request.body.decode())

        user_id = data["user_id"]
        gold_num = data["gold_num"]

        user = Client.objects.filter(wechat_id=user_id).update(gold=gold_num)
        if not user:
            return JsonResponse(data={'gold_status':False})
        return JsonResponse(data={"gold_status": True})


class UserListView(View):
    '''用户列表'''

    def post(self, request):
        users = Client.objects.all()
        content = []
        if users is not None:
            for user in users:
                result = user.to_dict()
                content.append(result)
        else:
            return JsonResponse(data={"msg": "没有查到用户信息"})

        return JsonResponse(data={"msg": content})
