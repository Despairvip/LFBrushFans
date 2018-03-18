from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from hashids import Hashids
from kuaishou_admin.models import Order, Client
import json
from django.core.paginator import Paginator

# Create your views here.
from utils.views import  login_admin_required_json

encrypt = Hashids()

'''登陆'''


def LoginView( request):
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


'''退出'''


@login_admin_required_json
def LogoutView( request):
    if request.method == "POST":
        logout(request)
        return JsonResponse(data={"msg": "logout success"})


'''实时订单查询'''


@login_admin_required_json
def RealOrdersView( request):
    '''实时订单，返回30条数据'''
    if request.method == "POST":
        if request.user.is_superuser:
            return JsonResponse(data={"msg": "未登录"})
        return HttpResponse("订单查询成功")


'''下拉框搜索'''


@login_admin_required_json
def OptionSearchView( request):
    # if not request.user.is_superuser:
    #     return JsonResponse(data={"msg": "未登录"})

    # 获取查询订单的类型(默认是所有订单类型)
    if request.method == "POST":
        data = json.loads(request.body.decode())

        detail_pro = data.get('detail_pro')
        print(detail_pro)
        order_type = data.get('order_type')
        print(order_type)
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
        elif detail_pro == '套餐订单' and order_type == '0':
            orders = Order.objects.filter(type_id=1).all()
        elif detail_pro == "套餐订单":
            orders = Order.objects.filter(type_id=1, status=order_type).all()
            print(orders)
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


'''输入框搜索 order'''


@login_admin_required_json
def EnterSearchView( request):
    if request.method == "POST":
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


'''用户名字/id 搜索'''


@login_admin_required_json
def UserSearchView( request):
    if request.method == "POST":
        '''搜索功能'''
        data = json.loads(request.body.decode())
        result = []
        print(data.get('user_id'))
        if data.get('user_id'):
            user_id = int(data.get("user_id")) - 1000
            if user_id < 0:
                return JsonResponse
            print(user_id)
            users = Client.objects.filter(id=user_id).all()
        else:
            users = Client.objects.filter(username=data.get("user_name")).all()

        if users:
            for user in users:
                content = user.to_dict()
                result.append(content)

        return JsonResponse(data={"msg": result})


'''修改订单状态'''


@login_admin_required_json
def ModifyStatusView( request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        order_status = data.get("order_status")
        hs_order_id = data.get('order_id')
        print(hs_order_id)
        order_id = encrypt.decode(hs_order_id)[0]
        print(order_id)

        order = Order.objects.filter(order_id_num=order_id).update(status=order_status)
        print(order)
        if not order:
            return JsonResponse(data={"msg": False})
        return JsonResponse({'msg': True})


'''修改金币'''


@login_admin_required_json
def ModifyGoldView( request):

    # 获取用户的id,和需要修改的金币数
    if request.method == "POST":
        data = json.loads(request.body.decode())

        user_id = data["user_id"]
        gold_num = data["gold_num"]
        try:
            user = Client.objects.filter(id=user_id).update(gold=gold_num)
        except Exception as e:
            return JsonResponse(data={"msg": "查不到用户"})
        if not user:
            return JsonResponse(data={'msg': False})

        return JsonResponse(data={'msg': True})


'''用户列表'''


@login_admin_required_json
def UserListView( request):
    # if not request.user.is_superuser:
    #     return JsonResponse(data={"msg": "未登录"})
    if request.method == "POST":
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
