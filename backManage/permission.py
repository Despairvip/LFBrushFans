'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/28/下午1:16
file:permission.py
IDE:PyCharm 
'''
import functools

from common.returnMessage import MessageResponse
from kuaishou_admin.models import Client

SUPERADMIN = ['admin', 'shiwei']


def decorator_to_permission(arg):
    '''
        权限装饰器
    :param arg:
    :return:
    '''
    if callable(arg):
        @functools.wraps(arg)
        def wrapper(*args, **kw):
            user = args[0].session.get("name")
            user_client = Client.objects.filter(username=user).first()
            if user_client is not None:
                if user_client.is_superuser:
                    outcome = arg(*args, **kw)
                else:
                    outcome = MessageResponse(3105)
            else:
                outcome = MessageResponse(3104)

            return outcome

        return wrapper
    else:
        def wrapper(func):
            @functools.wraps(func)
            def function(*args, **kw):

                if arg == "superadmin":

                    user = args[0].session.get("name")
                    print(user)
                    user_client = Client.objects.filter(username=user).first()

                    if user_client is not None:
                        if user_client.is_superuser and user in SUPERADMIN:
                            outcome = func(*args, **kw)
                        else:
                            outcome = MessageResponse(3105)
                    else:

                        outcome = MessageResponse(3104)

                return outcome

            return function

        return wrapper

# def decorator_to_gold_permission(arg):
#     def wrapper(func):
#
#         def function(*args,**kwargs):
#
#
#             outcome = func(*args,**kwargs)
#
#             return outcome
#
#         return function
#     return wrapper