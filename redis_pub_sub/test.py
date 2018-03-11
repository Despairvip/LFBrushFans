
from redis_pub_sub.lib_redis import RedisHelper

# 实例化RedisHelper类对象
obj = RedisHelper()

# 赋值订阅变量
redis_sub = obj.subscribe()

# 循环执行如下命令
while True:
    # 二次调用parse_response() 开始接收
    msg= redis_sub.parse_response()
    print(msg)


# 发消息加入频道
# obj.public('hello')
