'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
IDE:PyCharm
'''

from hashlib import md5
import time

from backManage.core import secret_to_userid

token = '9bf31c7ff062936a96d3c8bd1f8f2ff3-15'

secretid = token.split('-')[1]

print(token)

print(type(secret_to_userid(token)))