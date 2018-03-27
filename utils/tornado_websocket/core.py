'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/21/下午7:09
file:core.py
IDE:PyCharm 
'''

import hashlib
import hashids
import random

import time

from hashlib import md5
import time


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))


def dec2hex(string_num):
    base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('a'), ord('a') + 6)]
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])


ALPHABET = 'abcdef1234567890'
hashid = hashids.Hashids(alphabet=ALPHABET)


def userid_to_secret(id):
    userid = id
    s = hashid.encode(userid)
    return s
    # len_num = len(s) - len(dec2hex(hex2dec(s)))
    # if len_num > 0:
    #     result = '0'*len_num + dec2hex(hex2dec(s))
    #     print(s)
    #     print(userid,s,hex2dec(s),dec2hex(hex2dec(s)),hashid.decode(result))
    #     return s
    # else:
    #     print(s)
    #     print(userid,s,hex2dec(s),dec2hex(hex2dec(s)),hashid.decode(dec2hex(hex2dec(s))))
    #     result = dec2hex(hex2dec(s))
    #     return s


def secret_to_userid(secretid):
    len_num = len(secretid) - len(dec2hex(hex2dec(secretid)))
    if len_num > 0:
        result = '0' * len_num + dec2hex(hex2dec(secretid))
        return hashid.decode(result)[0]

    else:
        result = dec2hex(hex2dec(secretid))
        return hashid.decode(result)[0]


# res = userid_to_secret(1)
# s = secret_to_userid(res)
# print(type(s),s)

# h = hashlib.md5()
# print(time.time())


def create_token(id):
    id_secret = userid_to_secret(id)

    h1 = md5()
    h1.update(id_secret.encode(encoding='utf-8'))

    md_res = h1.hexdigest()
    print(md_res + '-' + id_secret)
    return md_res + '-' + id_secret


create_token(1)
