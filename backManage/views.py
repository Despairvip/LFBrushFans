import base64
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from backManage.libs_save_results import taocan_save, update_taocan_msg
from kuaishou_admin.models import Order_combo, Project, Client


@login_required
def proManage(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                proName = data["name"]
                proNum = data["num"]
                gold = data["gold"]

                if Project.objects.create(pro_name=proName,pro_gold=gold,count_project=proNum):
                    return JsonResponse({'status': 200})
            else:
                return JsonResponse({"status":500,"msg":"you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})



@login_required
def changeProManage(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                id = data['id']
                name = data['name']
                num = data['num']
                gold = data["gold"]

                project = Project.objects.filter(id=id).first()
                if project is None:
                    return JsonResponse({'status':500,'msg':'your project is not exists'})
                project.pro_name = name
                project.pro_gold = gold
                project.count_project = num
                project.save()
                return JsonResponse({
                    "status":0
                })
            else:
                return JsonResponse({"status":500,"msg":"you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def showProject(request):
    if request.method == "POST":
        user = request.session["name"]
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
                    pro_msg['count'] = project.pro_gold
                    data.append(pro_msg)
                return JsonResponse({"status":0,"data":data})
            else:
                return JsonResponse({"status":500,"msg":"you are not superuser"})
        else:
            return JsonResponse({"status":500,"msg":"usr is not exists"})
@login_required
def deleteProject(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                project_id = data['id']

                project = Project.objects.filter(id=project_id).first()
                if project is None:
                    return JsonResponse({'status':500,'msg':'project not exists'})
                project.delete()
                return JsonResponse({"status":0})
            else:
                return JsonResponse({"status":500,"msg":"you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})


@login_required
def taocanManage(request):
    if request.method == "POST":
        user = request.session["name"]
        user_client = Client.objects.filter(username=user).first()
        if user_client is not None:
            if user_client.is_superuser:
                data = json.loads(request.body.decode())
                print(data)
                taocan_name = data['name']
                taocan_gold = data['gold']

                projectOneName = data['detail'][0]['proName']
                projectOneNum = data['detail'][0]['num']

                projectTwoName = data['detail'][1]['proName']
                projectTwoNum = data['detail'][1]['num']

                projectThreeName = data['detail'][2]['proName']
                projectThreeNum = data['detail'][2]['num']


                if Order_combo.objects.filter(name=taocan_name).first():


                    return JsonResponse({"status":500,'msg':'already exists'})

                taocan = Order_combo.objects.create(name=taocan_name,pro_gold=taocan_gold)

                projectOne,projectTwo,projectThree = taocan_save(projectOneName,projectOneNum,projectTwoName,projectTwoNum,projectThreeName,projectThreeNum)
                taocan.detail_combo.add(projectOne,projectTwo,projectThree)
                taocan.save()
                return JsonResponse({"status":0})
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
                taocans = Order_combo.objects.all().prefetch_related('detail_combo')
                data = []
                for taocan in taocans:
                    taocan_msg = {}
                    taocan_msg['id'] = taocan.id
                    taocan_msg['name'] = taocan.name
                    taocan_msg['gold'] = taocan.pro_gold
                    # print("###########")
                    # print(taocan.detail_combo.all())
                    # print('(*********')
                    taocan_msg['detail'] = []
                    for detail in taocan.detail_combo.all():

                        taocan_msg['detail'].append({
                            'project_name':detail.pro_name,
                            'project_num':detail.pro_gold,
                            'project_id':detail.id,
                        })
                    data.append(taocan_msg)
                print(data)

                return JsonResponse({"data":data})
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
                taocan_id = data['id']
                taocan_name = data['name']
                taocan_gold = data['gold']

                projectOneName = data['detail'][0]['proName']
                projectOneNum = data['detail'][0]['num']
                projectOneid = data['detail'][0]['id']

                projectTwoName = data['detail'][1]['proName']
                projectTwoNum = data['detail'][1]['num']
                projectTwoid = data['detail'][1]['id']


                projectThreeName = data['detail'][2]['proName']
                projectThreeNum = data['detail'][2]['num']
                projectThreeid = data['detail'][2]['id']


                taocan = Order_combo.objects.filter(id=taocan_id).first()
                if taocan is None:
                    return JsonResponse({"status":500,"msg":"taocan not exsits"})
                proOne,proTwo,proThree = update_taocan_msg(
                    projectOneName,projectOneNum,projectOneid,
                    projectTwoName,projectTwoNum,projectTwoid,
                    projectThreeName,projectThreeNum,projectThreeid,
                )
                taocan.name = taocan_name
                taocan.pro_gold = taocan_gold


                taocan.detail_combo.add(proOne,proTwo,proThree)
                taocan.save()
                print(taocan.detail_combo.all())

                return JsonResponse({"status":0})
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
                    return JsonResponse({"status":500,'msg':'taocan is not exsits'})

                taocan.delete()
                return JsonResponse({"status": 0})
            else:
                return JsonResponse({"status": 500, "msg": "you are not superuser"})
        else:
            return JsonResponse({"status": 500, "msg": "usr is not exists"})





def login_houtai(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        user_name = data["user"]
        password = data["pwd"]
            # 认证用户
        user = authenticate(username=user_name, password=password)
        if user is None:
            return JsonResponse(data={"msg": False})

            # 保存用户登陆session信息
        request.session["name"] = user_name
        login(request,user)
        return JsonResponse(data={"msg": True})
    else:
        return JsonResponse({"msg":"please login"})







