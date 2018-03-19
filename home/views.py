from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt




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

    return JsonResponse(
        {
            "err": 0,
            "msg": "",
            "data": {
                "topbanner": [
                    {
                        "image": "https://www.apicloud.com/start_page/47/23/472344980350f56a6c9e377d29edc8ca.png",
                        "route":"CustomerService",
                        "type": 1,

                    },
                    {
                        "image": "https://www.apicloud.com/start_page/47/23/472344980350f56a6c9e377d29edc8ca.png",
                        "route":"",
                        "type": 2,

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

    return JsonResponse({
        "err":0,
        "msg":"",
        "data":{
            "numAndGold":[
                {

                    "num":200,
                    "gold":1000,

                },
                {
                    "num":200,
                    "gold":1000,

                },
                {
                    "num":200,
                    "gold":1000,

                },
                {
                    "num":200,
                    "gold":1000,

                },
                {
                    "num":200,
                    "gold":1000,

                },
                {
                    "num":200,
                    "gold":1000,

                },
            ]
        }
    })


@csrf_exempt
def remenTaocan(request):



    return JsonResponse(
        {
            "status":0,
            "msg":"",
            "data":{
                "taocan":[
                    {
                        "name":"套餐一",
                        "gold":800,
                        "detail":[
                            {"name":"双击",
                              "num":200
                             },
                            {"name":"评论",
                              "num":10
                             },
                            {"name":"播放",
                              "num":200
                             },
                        ]
                    },
                    {
                        "name":"套餐二",
                        "gold":1600,
                        "detail":[
                            {"name":"双击",
                              "num":500
                             },
                            {"name":"评论",
                              "num":20
                             },
                            {"name":"播放",
                              "num":5000
                             },
                        ]
                    },
                    {
                        "name":"套餐三",
                        "gold":3000,
                        "detail":[
                            {"name":"双击",
                              "num":800
                             },
                            {"name":"评论",
                              "num":50
                             },
                            {"name":"播放",
                              "num":1000
                             },
                        ]
                    },
                    {
                        "name":"套餐四",
                        "gold":5000,
                        "detail":[
                            {"name":"双击",
                              "num":1200
                             },
                            {"name":"评论",
                              "num":80
                             },
                            {"name":"播放",
                              "num":50000
                             },
                        ]
                    },
                    {
                        "name":"套餐五",
                        "gold":10000,
                        "detail":[
                            {"name":"双击",
                              "num":5000
                             },
                            {"name":"评论",
                              "num":150
                             },
                            {"name":"播放",
                              "num":15000
                             },
                        ]
                    },
                    {
                        "name":"套餐六",
                        "gold":20000,
                        "detail":[
                            {"name":"双击",
                              "num":10000
                             },
                            {"name":"评论",
                              "num":300
                             },
                            {"name":"播放",
                              "num":30000
                             },
                        ]
                    },


                ]
            }

        }
    )


@csrf_exempt
def shuafenshi(request):
    return JsonResponse(
        {
            "err":0,
            "msg":"",
            "data":{
                "numAndGold": [
                    {
                        "num": 200,
                        "gold": 1000,

                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                ]
            }
        }
    )


@csrf_exempt
def play_home_page(request):
    return JsonResponse(
        {
            "err":0,
            "msg":"",
            "data":{
                "numAndGold": [
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                    {
                        "num": 200,
                        "gold": 1000,
                        "verifylogin": True,
                    },
                ]
            }
        }
    )