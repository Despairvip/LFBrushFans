'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/21/上午11:26
file:returnMessage.py
IDE:PyCharm 
'''

from collections import namedtuple

from django.http import JsonResponse

code_msg_list = [
    (0,"成功"),
    (2001,"数据库查询错误"),
    (2002,"没有数据"),
    (2003,"数据已存在"),
    (2004,"数据错误"),
    (3101,"用户未登陆"),
    (3102,"用户登陆失败"),
    (3103,"用户参数错误"),
    (3104,"用户不存在"),
    (3105,"用户身份错误"),
    (3106,"密码错误"),
    (3107,"修改错误"),
    (4201,"未知错误"),
    (4202,"内部错误"),
    (4203,"版本需更新"),
    (4204,"第三方系统错误"),

]

code_msgs = namedtuple('code_msgs',["code","msg"])


def MessageResponse(num,msg=None,data=None):
    '''
    错误消息或者正确消息的重新返回处理
    :param num:
    :return:
    '''
    for code_msg in code_msg_list:
        code_msg_name = code_msgs._make(code_msg)
        if code_msg_name.code == num:

            if num == 0:
                if msg is None:
                    if data is None:
                        return JsonResponse({"status":num,"msg":code_msg_name.msg})
                    return JsonResponse({"status":num,"msg":code_msg_name.msg,"data":data})
                else:
                    if data is None:
                        return JsonResponse({"status": num, "msg": msg})
                    return JsonResponse({"status":num,"msg":msg,"data":data})
            if msg is None:
                return JsonResponse({"status":code_msg_name.code,"msg":code_msg_name.msg})
            else:
                return JsonResponse({"status":num,"msg":msg})

