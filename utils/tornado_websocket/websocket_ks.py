'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
IDE:PyCharm
'''

import base64
import os, django

import re
from django.template import base

from lib_redis import RedisHelper
import sfpt
import os

# os.environ.update({"DJANGO_SETTINGS_MODULE": "sftp.settings"})
#
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sfpt.settings")  # project_name 项目名称
django.setup()

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
from core import secret_to_userid
from kuaishou_admin.models import Client


# super_user = ["admin"]


# Tag = "_auth_user_id"



class WebSocketHandler(tornado.websocket.WebSocketHandler):
    executor = ThreadPoolExecutor(100)

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

    def open(self):
        self.islogin = False
        self.status_close = False



    @run_on_executor
    def on_message(self, message):

        obj_msg = json.loads(message)
        print(obj_msg)

        if hasattr(self,"event_"+obj_msg["action"]):
            print(getattr(self,"event_"+obj_msg["action"]))
            getattr(self,"event_"+obj_msg["action"])(obj_msg)
        else:
            #no attr
            print("no attr")
            pass


    def event_init(self,obj):
        print("ws",self)
        import json

        self.write_message(json.dumps(
            {'action': "start"}
        ))
        print(33333)

        token = obj.get("token")
        token = Client.objects.filter(token=token).first()
        if token:
            while not self.status_close:
                print(11)
                if self.status_close:
                    break
                obj = RedisHelper()
                redis_sub = obj.subscribe()
                data = redis_sub.get_message(True, 1)
                print(data)
                if data:
                    data_new = json.loads(data.get("data").decode())
                    print(type(data_new),data_new)
                    self.write_message({"action":"order","data":data_new})
                    print("***********")
                    continue

        else:
            self.write_message({"action": "noLogin"})
            time.sleep(1)
            try:
                self.close()
            except Exception:
                pass



    def on_close(self):
        self.status_close = True


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocketHandler),

        ]
        print("debug")
        tornado.web.Application.__init__(self, handlers, debug=True)


if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", action="store", type="int", default="8081")
    (options, args) = parser.parse_args()

    ws_app = Application()

    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
