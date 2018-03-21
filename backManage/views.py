'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:views.py
IDE:PyCharm
'''

import base64
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from backManage.libs_save_results import  save_taocan_detail, update_taocan, delete_pro_in_taocan
from kuaishou_admin.models import Order_combo, Project, Client


@login_required
def proManage(request):
    '''
    创建项目
    :param request:
    :return:
    '''
    if request.method == "POST":
        user = request.session.get("name")
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                proName = data["name"]
                proNum = data["num"]
                gold = data["gold"]
                proj = Project.objects.filter(pro_name=proName,pro_gold=gold,count_project=proNum)
                if proj is not None:
                    return JsonResponse({"status":500,"msg":"this project exists"})
                if Project.objects.create(pro_name=proName, pro_gold=gold, count_project=proNum):
                    return JsonResponse({'status': 0})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def changeProManage(request):
    """
    根据项目id修改项目
    :param request:
    :return:
    """
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                id = data.get("id")
                name = data.get("name")
                num = data.get("num")
                gold = data.get("gold")

                project = Project.objects.filter(id=id).first()
                if project is None:
                    return JsonResponse({'status': 500, 'msg': 'your project is not exists'})
                project.pro_name = name
                project.pro_gold = gold
                project.count_project = num
                project.save()
                return JsonResponse({
                    "status": 0
                })
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def showProject(request):
    """
    显示项目总类
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
                    pro_msg['id'] = project.id
                    pro_msg['name'] = project.pro_name
                    pro_msg['count'] = project.count_project
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
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                project_id = data.get("id")

                project = Project.objects.filter(id=project_id).first()
                if project is None:
                    return JsonResponse({'status': 500, 'msg': 'project not exists'})
                project.delete()
                return JsonResponse({"status": 0})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


# @login_required
def taocanManage(request):
    '''
    创建套餐
    :param request:
    :return:
    '''
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())

                # taocan_name = data['name']
                # taocan_gold = data['gold']
                #
                # projectOneName = data['detail'][0]['proName']
                # projectOneNum = data['detail'][0]['num']
                # print('********')
                # print(projectOneNum)
                #
                # projectTwoName = data['detail'][1]['proName']
                # projectTwoNum = data['detail'][1]['num']
                #
                # projectThreeName = data['detail'][2]['proName']
                # projectThreeNum = data['detail'][2]['num']
                result = save_taocan_detail(**data)

                if result["status"] == 0:
                    return JsonResponse({"status": 0})
                else:
                    return JsonResponse({"status": 500, "msg": result["msg"]})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def showTaocan(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                taocans = Order_combo.objects.all().prefetch_related('project_detail')
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


                return JsonResponse({"data": data})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def changeTaocan(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())


                result = update_taocan(**data)

                if result['status'] == 0:
                    return JsonResponse({"status": 0})
                else:
                    return JsonResponse({"status": 500, "msg": result["msg"]})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def deleteTaocan(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())

                taocan_id = data['id']

                taocan = Order_combo.objects.filter(id=taocan_id).first()
                if taocan is None:
                    return JsonResponse({"status": 500, 'msg': 'taocan is not exsits'})
                taocan.project_detail.clear()
                taocan.delete()
                return JsonResponse({"status": 0})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def delete_taocan_project(request):
    """
    移除套餐内的项目
    :param request:
    :return:
    """
    if request.method == "POST":
        data = json.loads(request.body.decode())

        result = delete_pro_in_taocan(**data)

        if result["status"] == 0:
            return JsonResponse({"status": 0})
        else:
            return JsonResponse({"status": result["status"], "msg": result["msg"]})


def login_houtai(request):
    """

    后台管理登陆
    :param request:
    :return:
    """
    if request.method == "POST":
        data = json.loads(request.body.decode())
        print(data)
        user_name = data.get("user")
        password = data.get("pwd")
        # 认证用户
        user = authenticate(username=user_name, password=password)
        if user is None:
            return JsonResponse(data={"msg": False})

            # 保存用户登陆session信息
        request.session["name"] = user_name
        login(request, user)
        return JsonResponse(data={"msg": True})
    else:
        return JsonResponse({"msg": "please login"})


def index(request):
    if request.method == "GET":
        return render(request, "kuaishou_admin/index.html")
