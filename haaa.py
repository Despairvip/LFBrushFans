import hashids
import random

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('a'),ord('a')+6)]

def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])
ALPHABET = 'abcdef1234567890'
hashid = hashids.Hashids(alphabet=ALPHABET)
for  i in range(1,99999):
    userid =i
    s = hashid.encode(userid)
    print(s)
    print(userid,s,hex2dec(s),dec2hex(hex2dec(s)),hashid.decode(dec2hex(hex2dec(s))))

    # print(s.encode('hex'))

