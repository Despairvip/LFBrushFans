
'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
IDE:PyCharm
'''

import base64
import os,django

import re
from django.template import base

from lib_redis import RedisHelper
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","sfpt/sfpt.settings")# project_name 项目名称
# django.setup()


import json
import time
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

# from django.contrib.sessions.models import Session


super_user = ["admin"]
# Tag = "_auth_user_id"





#TODO 需要验证身份才能使用
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    executor = ThreadPoolExecutor(10)


    def check_origin(self, origin):
        return True

    def open(self):
        # self.write_message("hahahahaha")
        self.status_close = False


    @run_on_executor
    def on_message(self,message):
        datas = [
            {
                "status_order": "未开始",
                "ordered_num": 200,
                "user_name": "Despair",
                "work_links": "www.baidu.com",
                "project_name": "刷粉订单",
                "order_id": "20180306024645100103440",
                "kuaishou_id": "k123456",
                "create_order_time": "2018-03-06T02:46:45.049Z"
            },
            {
                "status_order": "未开始",
                "ordered_num": 200,
                "user_name": "Deir",
                "work_links": "www.baidu.com",
                "project_name": "刷粉订单",
                "order_id": "20180306024100103440",
                "kuaishou_id": "k12345",
                "create_order_time": "2018-03-06T02:46:45.049Z"
            },
            {
                "status_order": "已开始",
                "ordered_num": 200,
                "user_name": "Despair",
                "work_links": "www.baidu.com",
                "project_name": "刷粉订单",
                "order_id": "2018030602100103440",
                "kuaishou_id": "k456",
                "create_order_time": "2018-03-06T02:46:45.049Z"
            },
            {
                "status_order": "未开始",
                "ordered_num": 100000,
                "user_name": "Despair",
                "work_links": "www.cc.com",
                "project_name": "刷粉订单",
                "order_id": "20180306024645100103440",
                "kuaishou_id": "k123456",
                "create_order_time": "2018-03-06T02:46:45.049Z"
            },
            {
                "status_order": "未开始",
                "ordered_num": 300,
                "user_name": "laowang",
                "work_links": "www.baidu.com",
                "project_name": "套餐一",
                "order_id": "123132131",
                "kuaishou_id": "123456",
                "create_order_time": "2018-03-06T00:00:00Z"
            },
            {
                "status_order": "未开始",
                "ordered_num": 5443,
                "user_name": "laoli",
                "work_links": "www.baidu.com",
                "project_name": "刷粉订单",
                "order_id": "32142431",
                "kuaishou_id": "1234567",
                "create_order_time": "2018-03-06T00:00:00Z"
            },
        ]
        obj = RedisHelper()
        obj_msg = json.loads(message)
        # session_key = self.get_cookie("name")
        # print(session_key)

        # 赋值订阅变量
        redis_sub = obj.subscribe()
        #
        # sessionid = self.get_cookie("sessionid")
        # print(sessionid)
        # session_key = Session.objects.filter(session_key=sessionid).first()
        # session_msg = session_key.session_data
        # user_msg = base64.b64decode(session_msg).decode()

        # print(user_msg)
        # search_msg = re.match( r'(.*) "name:" (.*?) .*', user_msg, re.M|re.I)
        # print(session_msg)
        # for i in super_user:
        #     if i in user_msg:


        if obj_msg['action'] == "start":
            # for i in super_user:
            #     if "admin" in i:
            # # 循环执行如下命令
            #         while not self.status_close:
            #             # 二次调用parse_response() 开始接收
            #             msg_json = redis_sub.parse_response(timeout = 1)[2]
            #             print(msg_json)
            #             msg = msg_json.decode()
            #             time.sleep(1)
            #             self.write_message(msg)
            #         print("结束循环")

            #TODO 这里还要判断是否断开连接 on_close不可靠
            while not self.status_close:
                data = redis_sub.get_message(True, 1)
                if data:
                    self.write_message(data)
            print("结束循环")







    def on_close(self):
        self.status_close = True




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocketHandler),


        ]
        print("debug")
        tornado.web.Application.__init__(self, handlers,debug = True)


if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", action="store", type="int", default="8081")
    (options, args) = parser.parse_args()


    ws_app = Application()

    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


