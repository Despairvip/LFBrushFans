'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
('third_name', models.CharField(default='', max_length=20)),
IDE:PyCharm
'''

import os
import sys

sys.path.append("/home/sfpt-server/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'sfpt.settings'  # 项目的settings
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import base64
import os

import re
from django.template import base

from lib_redis import RedisHelper
import os

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

    def on_message(self, message):
        print(message)

        obj_msg = json.loads(message)

        if hasattr(self, "event_" + obj_msg["action"]):
            getattr(self, "event_" + obj_msg["action"])(obj_msg)
        else:
            # no attr
            print("no attr")
            pass

    def event_HeartBeat(self, obj):
        self.write_message({"action": "HeartBeat"})

    @run_on_executor
    def event_init(self, obj):
        print("ws", self)
        import json

        self.write_message(json.dumps(
            {'action': "start"}
        ))

        token = obj.get("token")
        token = Client.objects.filter(token=token).first()
        if token and token.is_superuser:
            while not self.status_close:
                if self.status_close:
                    break
                obj = RedisHelper()
                redis_sub = obj.subscribe()
                data = redis_sub.get_message(True, 1)
                if data:
                    data_new = json.loads(data.get("data").decode())
                    self.write_message({"action": "order", "data": data_new})
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
