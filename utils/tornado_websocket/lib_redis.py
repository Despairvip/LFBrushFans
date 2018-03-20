'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
IDE:PyCharm
'''



import redis

class RedisHelper:

    def __init__(self):
        # 链接服务端
        self.__conn = redis.Redis(host='127.0.0.1')

        # 加入两个频道
        self.chan_sub = 'fm104.5'
        self.chan_pub = 'fm104.5'

    def public(self, msg):
        #发消息订阅方
        # publish发消息加入频道chan_pub
        self.__conn.publish(self.chan_pub, msg)
        return True

    def subscribe(self):
        # 开始订阅pubsub()
        # 打开收音机
        pub = self.__conn.pubsub()

        # 调频道 subscribe
        pub.subscribe(self.chan_sub)

        # 准备接收parse_response()
        # 在次调用parse_response() 开始接收
        pub.parse_response()

        # 返回订阅变量
        return pub

