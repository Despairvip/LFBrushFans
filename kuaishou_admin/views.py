from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from hashids import Hashids
from kuaishou_admin.models import Order, Client
import json
from django.core.paginator import Paginator

# Create your views here.
from utils.views import LoginRequiredJsonMixin

encrypt = Hashids()


class LoginView(View):
    '''登陆'''

    def post(self, request):
        data = json.loads(request.body.decode())
        user_name = data["user"]
        password = data["pwd"]
        # 认证用户
        user = authenticate(username=user_name, password=password)
        if user is None:
            return JsonResponse(data={"msg": False})

        # 保存用户登陆session信息
        login(request, user)
        # 跳转到主页
        return JsonResponse(data={"msg": True})


class LogoutView(View, LoginRequiredJsonMixin):
    '''退出'''

    def post(self, request):
        logout(request)
        return JsonResponse(data={"msg": "logout success"})


class RealOrdersView(View, LoginRequiredJsonMixin):
    '''实时订单查询'''

    # @login_required
    def post(self, request):
        '''实时订单，返回30条数据'''

        return HttpResponse("订单查询成功")


class OptionSearchView(View, LoginRequiredJsonMixin):
    '''下拉框搜索'''
    def post(self, request):
        if not request.user.is_superuser:
            return JsonResponse(data={"msg":"用户未登录"})
        else:
            # 获取查询订单的类型(默认是所有订单类型)
            data = json.loads(request.body.decode())

            detail_pro = data.get('detail_pro')
            order_type = data.get('order_type')
            page = data.get("page", 1)
            # 一页几条数据
            num_page = data.get("num_page", 10)

            try:
                num_page = int(num_page)
                page = int(page)

            except Exception as e:
                print(e)

            if detail_pro == "所有项目" and order_type == "0":
                orders = Order.objects.all()
            elif detail_pro == "所有项目":
                orders = Order.objects.filter(status=order_type).all()
            elif detail_pro == "套餐订单":
                orders = Order.objects.filter(type_id=1, status=order_type).all()
            else:
                if order_type == '0':
                    orders = Order.objects.filter(project__pro_name__exact=detail_pro).all()
                else:
                    orders = Order.objects.filter(project__pro_name__exact=detail_pro, status=order_type).all()

            result = []
            for order in orders:
                if order.project:
                    content = order.to_dict()
                    content["project_name"] = order.project.pro_name
                    order_id = content['order_id']
                    hs_order_id = encrypt.encode(int(order_id))
                    content['order_id'] = hs_order_id
                    result.append(content)
                else:

                    content = order.to_dict()
                    content["project_name"] = order.combo.name
                    order_id = content['order_id']
                    hs_order_id = encrypt.encode(int(order_id))
                    content['order_id'] = hs_order_id

                    result.append(content)
            p = Paginator(result, num_page)
            count = p.count
            pages = p.num_pages
            pages_ss = p.page(page).object_list
            return JsonResponse(data={"msg": pages_ss, "count": count, "pages": pages})


class EnterSearchView(View, LoginRequiredJsonMixin):
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
                order_id = content['order_id']
                hs_order_id = encrypt.encode(int(order_id))
                content['order_id'] = hs_order_id

                message.append(content)
        else:
            return JsonResponse(data={"msg": "wrong format"})

        return JsonResponse(data={'msg': message})


class UserSearchView(View, LoginRequiredJsonMixin):
    '''用户名字/id 搜索'''

    def post(self, request):
        '''搜索功能'''
        data = json.loads(request.body.decode())
        try:
            orders = Order.objects.filter(client__wechat_id__exact=data["user_id"]).all()
        except:
            orders = Order.objects.filter(client__name__exact=data["user_name"]).all()
        result = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = order.order_id_num
                # 把这个id加密
                hash_order_id = encrypt.encode(int(order_id))
                content['order_id'] = hash_order_id
                result.append(content)

        return JsonResponse(data={"msg": result})


class ModifyStatusView(View, LoginRequiredJsonMixin):
    '''修改订单状态'''

    def post(self, request):
        data = json.loads(request.body.decode())

        order_status = data["order_status"]
        hs_order_id = data['order_id']
        order_id = encrypt.decode(hs_order_id)[0]

        order = Order.objects.filter(order_id_num=order_id).update(status=order_status)
        if not order:
            return JsonResponse(data={"msg": False})
        return JsonResponse({'msg': True})


class ModifyGoldView(View, LoginRequiredJsonMixin):
    '''修改金币'''

    def post(self, request):
        # 获取用户的id,和需要修改的金币数
        data = json.loads(request.body.decode())

        user_id = data["user_id"]
        gold_num = data["gold_num"]

        user = Client.objects.filter(wechat_id=user_id).update(gold=gold_num)
        if not user:
            return JsonResponse(data={'msg': False})

        return JsonResponse(data={'msg': True})


class UserListView(View, LoginRequiredJsonMixin):
    '''用户列表'''

    def post(self, request):
        users = Client.objects.all().order_by('-gold')
        content = []
        if users is not None:
            for user in users:
                result = user.to_dict()
                content.append(result)
        else:
            return JsonResponse(data={"msg": "没有查到用户信息"})
        p = Paginator(content, 30)
        pages_ss = p.page(1).object_list
        return JsonResponse(data={"msg": pages_ss})
