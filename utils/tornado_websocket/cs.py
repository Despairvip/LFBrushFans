'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/28/下午5:23
file:cs.py
IDE:PyCharm 
'''

from utils.tornado_websocket.lib_redis import RedisHelper

while True:
    obj = RedisHelper()
    redis_sub = obj.subscribe()
    data = redis_sub.get_message(True, 1)
    print(data)