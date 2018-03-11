# -*- coding:utf-8 -*-
import json

from redis_pub_sub.lib_redis import RedisHelper
# 实例化对象
obj = RedisHelper()

# 发消息加入频道
msg_json = json.dumps({'name':'zz'})
obj.public(msg_json)