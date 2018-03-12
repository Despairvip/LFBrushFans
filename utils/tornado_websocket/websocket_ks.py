import json
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from utils.redis_pub_sub.lib_redis import RedisHelper


class WebSocketHandler(tornado.websocket.WebSocketHandler):


    def check_origin(self, origin):
        return True

    def open(self):
        # self.write_message("hahahahaha")
        self.status_close = False


    # @run_on_executor
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
        obj = json.loads(message)

        # 赋值订阅变量
        redis_sub = obj.subscribe()

        if obj['action'] == "start":

            # 循环执行如下命令
            while not self.status_close:
                # 二次调用parse_response() 开始接收
                msg_json = redis_sub.parse_response()[2]
                print(msg_json)
                msg = json.dumps(msg_json.decode())

                time.sleep(1)
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


