import json
import logging
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger("django_app")
from kuaishou_admin.models import Project, Order_combo, Client


@csrf_exempt
def page_shuafen_pay(request):
    return JsonResponse(
        {
            {'status':200,
             'type':1,
             'data':{
                 'pay':''
             }


             },
        }
    )


@csrf_exempt
def home(request):
    version_code = json.loads(request.body.decode()).get("version_code")
    try:
        version_num = Client.objects.values("version").first().get('version')
        print(version_num)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status":4001})
    if version_code < version_num:
        return JsonResponse(data={"status":0,"msg":'用户需要更新软件'})

    return JsonResponse(
        {
            "err": 0,
            "msg": "",
            "data": {
                "topbanner": [
                    {
                        "image": "https://www.apicloud.com/start_page/47/23/472344980350f56a6c9e377d29edc8ca.png",
                        "parms": {
                            "name": "HelpPage"
                        },
                        "type": 2,
                        "verifylogin": False
                    },
                    {
                        "image": "https://www.apicloud.com/start_page/47/23/472344980350f56a6c9e377d29edc8ca.png",
                        "parms": {
                            "name": "AboutMe"
                        },
                        "type": 2,
                        "verifylogin": False
                    }
                ],
                "app": [
                    {
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexFans.png",
                        "title": "快手粉丝",
                        "route": "KsFans"
                    },
                    {
                        "title": "快手播放量",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexPlay.png",
                        "route": "KsPlay"
                    },
                    {
                        "title": "快手双击",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexClick.png",
                        "route": "KsDoubleClick"
                    },
                    {
                        "title": "快手直播号",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexAccount.png",
                        "route": "KsAccount"
                    },
                    {
                        "title": "热门套餐",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexHot.png",
                        "route": "ksHotCombo"
                    },
                    {
                        "title": "无水印下载",
                        "image": "http://oxrm6w8zc.bkt.clouddn.com/indexDownload.png",
                        "route": "KsDownload"
                    }
                ]
            }
        }
    )

@csrf_exempt
def shuangji_page(request):
    try:
        clicks = Project.objects.filter(pro_name="刷双击").all()
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status":4001,"msg":"数据哭查询失败"})
    content=[]
    if clicks:
        for fan in clicks:
            content.append(fan.to_dict())

    return JsonResponse(data={"status":0,"data":content})


@csrf_exempt
def remenTaocan(request):
    try:
        clicks = Order_combo.objects.all()
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status": 4001, "msg": "数据哭查询失败"})
    content = []
    if clicks:
        for fan in clicks:
            content.append(fan.to_dict())

    return JsonResponse(data={"status": 0, "data": content})


@csrf_exempt
def shuafenshi(request):
    try:
        fans = Project.objects.filter(pro_name="刷粉丝").all()
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status":4001,"msg":"数据哭查询失败"})
    content=[]
    if fans:
        for fan in fans:
            content.append(fan.to_dict())

    return JsonResponse(data={"status":0,"data":content})







@csrf_exempt
def play_home_page(request):
    try:
        fans = Project.objects.filter(pro_name="刷播放").all()
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"status":4001,"msg":"数据哭查询失败"})
    content=[]
    if fans:
        for fan in fans:
            content.append(fan.to_dict())

    return JsonResponse(data={"status":0,"data":content})
