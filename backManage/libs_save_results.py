'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
IDE:PyCharm
'''
import logging

from django.http import JsonResponse

from kuaishou_admin.models import Order_combo, Combo_project, Client

logger = logging.getLogger("django_admin")


def save_taocan_detail(**kwargs):
    """
    创建套餐及其中的数据
    :param kwargs:
    :return:
    """

    taocan_name = kwargs.get("name")
    taocan_gold = kwargs.get("gold")
    taocan_detail = kwargs.get("detail")
    if Order_combo.objects.filter(name=taocan_name).first():
        return {"status": 500, 'msg': 'already exists'}
    try:
        taocan = Order_combo.objects.create(name=taocan_name,pro_gold=taocan_gold)
    except Exception as e:
        taocan.delete()
        logger.error(e)
        return {"status":500,"msg":"创建套餐错误"}

    msg_status = []
    for msg in taocan_detail:

        try:
            project = Combo_project.objects.get_or_create(pro_name=msg.get("project_name"),
                                                          count_project=msg.get("project_num"))

        except Exception as e:
            logger.error(e)
            return {"status": 500, "msg": "创建项目错误"}
        taocan.project_detail.add(project[0].id)
        msg_status.append(project[1])



    if any(msg_status):
        taocan.save()

        return {"status": 0, 'msg': 'create data success'}
    else:
        taocan.delete()
        return {"status": 500, 'msg': 'create data failed'}







def update_taocan(**kwargs):
    """
    修改套餐信息
    :param kwargs:
    :return:
    """
    taocan_name = kwargs.get("name")
    taocan_gold = kwargs.get("gold")
    taocan_id = kwargs.get("combo_id")

    taocan_detail = kwargs.get("detail")
    try:
        taocan = Order_combo.objects.filter(id=taocan_id).first()
    except Exception as e:
        logger.error(e)
        return {"status": 500, "msg": "查询套餐失败"}
    else:
        taocan.project_detail.clear()

    for msg in taocan_detail:
        try:
            project_new = Combo_project.objects.get_or_create(pro_name=msg.get("project_name"),
                                                          count_project=msg.get("project_num"))
        except Exception as e:
            logger.error(e)
            return {"status":500,"msg":"创建项目失败"}
        else:
            taocan.project_detail.add(project_new[0].id)


    taocan.name = taocan_name
    taocan.pro_gold = taocan_gold
    taocan.save()
    return {"status":0}





# def auth_super(func):
#     def func(request,*args,**kwargs):
#         user = request.session.get("name")
#         user_client = Client.objects.filter(username=user).first()
#         if user_client is not None:
#             if user_client.is_superuser:
#                 return func(request,*args,**args)
#
#
#
#
#
#     return func







