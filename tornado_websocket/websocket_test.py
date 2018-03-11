import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
import json

import redis

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor




redisconn = redis.Redis(host="127.0.0.1", port=6379)
msg = json.dumps({
    'name':'zz',
    'age':18,
})
redisconn.rpush("manage:list:user",msg)



class WebSocketHandler(tornado.websocket.WebSocketHandler):
    executor = ThreadPoolExecutor(500)

    def check_origin(self, origin):
        return True

    def open(self):
        self.status_close = False
        pass

    @run_on_executor
    def on_message(self,message):
        user_id = self.get_secure_cookie('secretkey')
        sub = redisconn.pubsub()

        msg = redisconn.lrange('message:list:%s'%user_id,0,-1)
        msg_new = msg.decode()
        # if data:
        self.write_message(msg)




    def on_close(self):
        self.status_close = True


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocketHandler)
        ]
        tornado.web.Application.__init__(self, handlers)







if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8081)
    tornado.ioloop.IOLoop.instance().start()
