import logging
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from hashids import Hashids
from kuaishou_admin.models import Order, Client, AdminManagement, CheckVersion, Project
import json
from django.core.paginator import Paginator


# Create your views here.
from utils.views import login_admin_required_json, expired_message
expired_message()
encrypt = Hashids()
logger = logging.getLogger("django_admin")
'''登陆'''

'''
这是老的：xialing
新的在backmanage里面：zhouzhou

'''

# @login_admin_required_json


'''退出'''


@login_admin_required_json
def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse(data={"msg": "logout success"})


'''实时订单查询'''


@login_admin_required_json
def RealOrdersView(request):
    '''实时订单，返回30条数据'''
    if request.method == "POST":
        if request.user.is_superuser:
            return JsonResponse(data={"msg": "未登录"})
        return HttpResponse("订单查询成功")


'''下拉框搜索'''

"""
xialing

"""


@login_admin_required_json
def OptionSearchView(request):
    # if not request.user.is_superuser:
    #     return JsonResponse(data={"msg": "未登录"})

    # 获取查询订单的类型(默认是所有订单类型)
    if request.method == "POST":
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
            return JsonResponse(data={"status": 3103, "msg": "数据错误", })

        if detail_pro == "所有项目" and order_type == "0":
            orders = Order.objects.all()
        elif detail_pro == "所有项目":
            orders = Order.objects.filter(status=order_type).all()
        elif detail_pro == '套餐订单' and order_type == '0':
            orders = Order.objects.filter(type_id=1).all()
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


'''输入框搜索 order'''
'''
xialing and zhouzhou

'''


@login_admin_required_json
def EnterSearchView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        if "kuaishou_id" in data:
            kuaishou_id = data.get('kuaishou_id')

            orders = Order.objects.filter(kuaishou_id=kuaishou_id).all()
        else:
            message = []
            hs_order_id = data.get("order_id")
            order_id = encrypt.decode(hs_order_id)[0]

            order = Order.objects.get(order_id_num=order_id)
            content = order.to_dict()
            order_id = content['order_id']
            if order.project is None:
                content["project_name"] = order.combo.name
            else:
                content["project_name"] = order.project.pro_name
            hs_order_id = encrypt.encode(int(order_id))
            content['order_id'] = hs_order_id

            message.append(content)
            return JsonResponse(data={'msg': message})

        message = []
        if orders:
            for order in orders:
                content = order.to_dict()
                order_id = content['order_id']
                if order.project is None:
                    content["project_name"] = order.combo.name
                else:
                    content["project_name"] = order.project.pro_name
                hs_order_id = encrypt.encode(int(order_id))
                content['order_id'] = hs_order_id

                message.append(content)
        else:
            return JsonResponse(data={"msg": "wrong format"})

        return JsonResponse(data={'msg': message})


'''用户名字/id 搜索'''
'''
zhouzhou xialing

'''
import home.views
def combo_list():
    return  home.views.remenTaocan()



@login_admin_required_json
def UserSearchView(request):
    if request.method == "POST":
        '''搜索功能'''
        data = json.loads(request.body.decode())
        result = []

        if data.get('user_id'):
            user_id = int(data.get("user_id")) - 1000
            if user_id < 0:
                return JsonResponse

            users = Client.objects.get(id=user_id)
        else:
            user_name = data.get("user_name")
            users = Client.objects.get(name=user_name)


        if users:
            content = users.to_dict()
            result.append(content)
        else:
            return JsonResponse(data={"status" : 3103,"msg" : "输入有误"})
        return JsonResponse(data={"msg": result})


'''修改订单状态'''
'''
xialing

'''


@login_admin_required_json
def ModifyStatusView(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        order_status = data.get("order_status")
        hs_order_id = data.get('order_id')

        order_id = encrypt.decode(hs_order_id)[0]

        order = Order.objects.filter(order_id_num=order_id).update(status=order_status)

        if not order:
            return JsonResponse(data={"msg": False})
        return JsonResponse({'msg': True})


'''修改金币'''

'''
xialing

'''


@login_admin_required_json
def ModifyGoldView(request):
    # 获取用户的id,和需要修改的金币数
    if request.method == "POST":
        data = json.loads(request.body.decode())

        user_id = data.get("user_id")
        gold_num = data.get("gold_num")
        try:
            user = Client.objects.filter(id=user_id).update(gold=gold_num)
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"msg": "查不到用户"})
        if not user:
            return JsonResponse(data={'msg': False})

        return JsonResponse(data={'msg': True})


'''用户列表'''

'''
xialing
'''


@login_admin_required_json
def UserListView(request):
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


'''
written by Despair
'''


@login_admin_required_json
def add_wechat(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        wechat_id = data.get("wechat_id")
        type = data.get("type")  # 判断是增加微信号还是删除微信号
        if wechat_id and type is None:
            return JsonResponse(data={"status": 3103, "msg": "参数不全"})
        admin_set = AdminManagement.objects.filter(wechat=wechat_id)
        if type == 1:
            admin = admin_set.first()
            if admin is not None:
                if admin.isdelete == 0:
                    return JsonResponse(data={"status": 0, "msg": "此微信号已添加"})
            try:
                admins = AdminManagement()
                admins.wechat = wechat_id
                admins.save()
            except Exception as e:
                logger.error(e)
                return JsonResponse(data={"status": 4001, "msg": "修改错误"})
            return JsonResponse(data={"status": 0, "msg": "添加成功"})
        elif type == 2:
            if admin_set.first() is None:
                return JsonResponse(data={"status": 3103, "msg": "输入正确的信息"})

            try:
                admin_set.delete()
            except Exception as e:
                logger.error(e)
                return JsonResponse(data={"status": 2001, "msg": "操作失败"})
            return JsonResponse(data={"status": 0})
        else:
            return HttpResponseRedirect("http://yuweining.cn/t/Html5/404html/")


'''
written by Despair
'''


@login_admin_required_json
def new_version_update(request):
    '''版本更新'''
    data = json.loads(request.body.decode())
    version_code = data.get("version_code")
    sdk_url = data.get("sdk_url")
    update_msg = data.get("update_msg")

    try:
        version_query = CheckVersion.objects.first()
        if version_query is None :
            version = CheckVersion()
            version.version = version_code
            version.sdk_url = sdk_url
            version.upupdate_msg = update_msg
            version.save()
            return JsonResponse(data={"status": 0, "msg": "添加成功"})

    except Exception as e:

        logger.error(e)
        return JsonResponse(data={"status" : 2103,"msg" : "输入错误"})
    try:
        CheckVersion.objects.update(version=version_code, sdk_url=sdk_url, update_msg=update_msg)

    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status": 3107, "msg": "修改失败"})

    return JsonResponse(data={"status": 0})


"所有项目"


def all_project(request):
    names = Project.objects.values("pro_name").all()
    content = set()
    for pro_name in names:
        name = pro_name.get('pro_name')
        content.add(name)
    result = []
    for a in content:
        result.append(a)
    return JsonResponse(data={"status": 0, "data": result})


