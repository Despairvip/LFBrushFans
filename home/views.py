
import logging


from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django_app")
from kuaishou_admin.models import Project, Order_combo, Client, AdminManagement
from django.core.cache import cache

@csrf_exempt
def page_shuafen_pay(request):
    return JsonResponse(
        {
            {'status': 200,
             'type': 1,
             'data': {
                 'pay': ''
             }

             },
        }
    )


@csrf_exempt
def home(request):
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
    content = cache.get("click")
    if content is None:

        try:
            clicks = Project.objects.filter(pro_type=2).all()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
        content = []
        if clicks:
            for fan in clicks:
                content.append(fan.to_dict())
        cache.set("click",content,84600)
    return JsonResponse(data={"status": 0, "data": content})


@csrf_exempt
def remenTaocan(request):
    if request.method == "GET":
        taocans = Order_combo.objects.all().prefetch_related('project_detail')

        data = cache.get("combo")
        if data is None:
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
            # 缓存到数据库
            cache.set("combo",data,86400)
        return JsonResponse({"status": 0, "data": data})


@csrf_exempt
def shuafenshi(request):
    content = cache.get("fans")
    if content is None:
        try:
            fans = Project.objects.filter(pro_type=1).all()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
        content = []
        if fans:
            for fan in fans:
                content.append(fan.to_dict())
        cache.set("fans",content,86400)
    return JsonResponse(data={"status": 0, "data": content})


@csrf_exempt
def play_home_page(request):
    content = cache.get('play')
    if content is None:
        try:
            fans = Project.objects.filter(pro_type=3).all()
        except Exception as e:
            logger.error(e)
            return JsonResponse(data={"status": 4001, "msg": "数据库查询失败"})
        content = []
        if fans:
            for fan in fans:
                content.append(fan.to_dict())
        cache.set("play",content,86400)
    return JsonResponse(data={"status": 0, "data": content})
