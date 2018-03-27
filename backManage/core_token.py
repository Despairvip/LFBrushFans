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

from sfpt.settings_base import SECRET_APP


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
    count = 0
    s = hashid.encode(userid)

    for i in s:
        if i == '0':
            count += 1
        else:
            break

    if count > 0:
        return 'C' + str(count) + hex2dec(s)
    else:
        return hex2dec(s)


def secret_to_userid(secretid):
    if secretid.startswith('C'):
        num_zero = secretid[1]

        new_secretid = secretid[2:]
        secretid_dec = dec2hex(new_secretid)

        final_secretid = '0' * int(num_zero) + str(secretid_dec)

        return hashid.decode(final_secretid)

    else:
        return hashid.decode(dec2hex(secretid))


def create_token(id):
    id_secret = userid_to_secret(id)

    str_md = id_secret + str(time.time()) + SECRET_APP
    h1 = md5()
    h1.update(str_md.encode(encoding='utf-8'))

    md_res = h1.hexdigest()
    return md_res + '-' + id_secret


create_token(42)
