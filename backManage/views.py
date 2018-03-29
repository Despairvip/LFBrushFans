'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:views.py
IDE:PyCharm
'''

import base64
import json
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from backManage.core import create_token
from backManage.libs_save_results import save_taocan_detail, update_taocan
from backManage.permission import decorator_to_permission
from common.returnMessage import MessageResponse
from kuaishou_admin.models import Order_combo, Project, Client, MoneyAndGold

logger = logging.getLogger("django_admin")

@login_required
def proManage(request):
    '''
    创建项目
    :param request:
    :return:
    '''
    if request.method == "POST":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                proName = data.get("name")
                proNum = data.get("project_num")
                gold = data.get("gold")

                try:
                    proj = Project.objects.filter(pro_name=proName, pro_gold=gold, count_project=proNum).first()
                except Exception as e:
                    logger.error(e)
                    return MessageResponse(2001)
                if proj is not None:
                    return MessageResponse(2003)
                if Project.objects.create(pro_name=proName, pro_gold=gold, count_project=proNum):
                    return MessageResponse(0)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)


@login_required
def changeProManage(request):
    """
    根据项目id修改项目
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                id = data.get("pro_id")
                name = data.get("name")
                num = data.get("num")
                gold = data.get("gold")

                try:
                    project = Project.objects.filter(id=id).first()
                except Exception as e:
                    logger.error(e)
                    return MessageResponse(2001)
                if project is None:
                    return MessageResponse(2002)
                project.pro_name = name
                project.pro_gold = gold
                project.count_project = num
                project.save()
                return MessageResponse(0)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)


@login_required
def ShowAll(request):
    """
    显示所有的项目（套餐和小项目）
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                projects = Project.objects.all()
                data = []

                for project in projects:
                    pro_msg = {}
                    pro_msg["detail"] = {}
                    pro_msg['pro_id'] = project.id
                    pro_msg['name'] = project.pro_name
                    pro_msg['detail']['num'] = project.count_project
                    pro_msg['gold'] = project.pro_gold
                    data.append(pro_msg)
                taocans = Order_combo.objects.all().prefetch_related('project_detail')

                for taocan in taocans:
                    taocan_msg = {}
                    taocan_msg['combo_id'] = taocan.id
                    taocan_msg['name'] = taocan.name
                    taocan_msg['gold'] = taocan.pro_gold

                    taocan_msg['detail'] = []
                    for detail in taocan.project_detail.all():
                        taocan_msg['detail'].append({
                            'project_name': detail.pro_name,
                            'project_num': detail.count_project,
                            'project_id': detail.id,
                        })
                    data.append(taocan_msg)
                return MessageResponse(0, data=data)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)


# @login_required
def showProject(request):
    """
    显示全部项目
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.session.get("name")
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                projects = Project.objects.all()
                data = []
                # print(request.session["name"])
                for project in projects:
                    pro_msg = {}
                    pro_msg["detail"] = {}
                    pro_msg['id'] = project.id
                    pro_msg['name'] = project.pro_name
                    pro_msg['detail']['num'] = project.count_project
                    pro_msg['gold'] = project.pro_gold
                    data.append(pro_msg)
                return JsonResponse({"status": 0, "data": data})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def deleteProject(request):
    """
    删除项目
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                project_id = data.get("pro_id")
                try:
                    project = Project.objects.filter(id=project_id).first()
                except Exception as e:
                    logger.error(e)
                    return MessageResponse(2002)
                if project is None:
                    return MessageResponse(2002)
                project.delete()
                return MessageResponse(0)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)


@login_required
def taocanManage(request):
    '''
    创建套餐
    :param request:
    :return:
    '''
    if request.method == "POST":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())

                result = save_taocan_detail(**data)

                if result["status"] == 0:
                    return MessageResponse(0)
                else:
                    return MessageResponse(4202,msg=result["msg"])
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)

# @decorator_to_permission('superadmin')
# @login_required
def showTaocan(request):
    if request.method == "GET":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                try:
                    taocans = Order_combo.objects.all().prefetch_related('project_detail')
                except Exception as e:
                    logger.error(e)
                    return {"status":500,"msg":"查询失败"}
                data = []
                for taocan in taocans:
                    taocan_msg = {}
                    taocan_msg['id'] = taocan.id
                    taocan_msg['name'] = taocan.name
                    taocan_msg['gold'] = taocan.pro_gold

                    taocan_msg['detail'] = []
                    for detail in taocan.project_detail.all():
                        taocan_msg['detail'].append({
                            'project_name': detail.pro_name,
                            'project_num': detail.count_project,
                            'project_id': detail.id,
                        })
                    data.append(taocan_msg)
                # return render(request,'debug_test/debug_test.html',locals())
                return JsonResponse({"data": data[::-1]})
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)


@login_required
def changeTaocan(request):
    if request.method == "POST":
        user = request.session.get("name")
        try:
            user_client = Client.objects.filter(username=user).first()
        except Exception as e:
            logger.error(e)
            return MessageResponse(2001)
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())

                result = update_taocan(**data)

                if result['status'] == 0:
                    return MessageResponse(0)
                else:
                    return MessageResponse(2001)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)








@login_required
def deleteTaocan(request):
    if request.method == "POST":
        user = request.session.get("name")
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())

                taocan_id = data.get('combo_id')
                try:
                    taocan = Order_combo.objects.filter(id=taocan_id).first()
                except Exception as e:
                    logger.error(e)
                    return MessageResponse(2001)
                if taocan is None:
                    return MessageResponse(2002,msg="套餐是空的")
                taocan.project_detail.clear()
                taocan.delete()
                return MessageResponse(0)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)





def login_houtai(request):
    """

    后台管理登陆
    :param request:
    :return:
    """
    if request.method == "POST":
        data = json.loads(request.body.decode())
        user_name = data.get("user")
        password = data.get("pwd")
        # 认证用户
        user = authenticate(username=user_name, password=password)
        if user is None:
            return JsonResponse(data={"msg": False})

            # 保存用户登陆session信息
        request.session["name"] = user_name
        login(request, user)

        userid = request.user.id
        token = create_token(userid)
        print(token)
        request.user.token = token
        request.user.save()
        print(request.user.token)
        return MessageResponse(0,data=token)
    else:
        return JsonResponse({"msg": "please login"})


def index(request):
    if request.method == "GET":
        return render(request, "kuaishou_admin/index.html")



@decorator_to_permission('superadmin')
@login_required
def set_gold_money(request):
    '''
    设置积分和钱的配比
    :param request:
    :return:
    '''
    if request.method == "POST":
        user = request.session.get("name")
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                money = data.get("money")

                gold = data.get("gold")
                try:

                    try:
                        moneyAndGold = MoneyAndGold.objects.get_or_create(money=money,gold=gold)
                    except Exception as e:
                        logger.error(e)
                        return MessageResponse(2001)

                    if moneyAndGold[1] is False:
                        return MessageResponse(2003)
                    else:
                        data_list = []
                        data_dict = {}

                        data_dict["money"] = moneyAndGold[0].money
                        data_dict["gold"] = moneyAndGold[0].gold
                        data_dict["id"] = moneyAndGold[0].id
                        data_list.append(data_dict)
                        return MessageResponse(0, data=data_list)

                except Exception as e:
                    logger.error(e)
                    return MessageResponse(2001)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)



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
                data_dict["id"] = detial.id
                data.append(data_dict)

            return MessageResponse(0,data=data)

@login_required
def del_gold_money(request):
    """
    删除金钱和积分
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.session.get("name")
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                id = data.get("id")
                if isinstance(id,int):
                    try:
                        moneyAndGold = MoneyAndGold.objects.filter(id=id).first()
                    except Exception as e:
                        logger.error(e)
                        return MessageResponse(2001)
                    if moneyAndGold is None:
                        return MessageResponse(2002)
                    else:

                        moneyAndGold.delete()
                        return MessageResponse(0)
            else:
                return MessageResponse(3105)
        else:
            return MessageResponse(3104)














