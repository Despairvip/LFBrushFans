'''
ower:@shadoesmilezhou
email:630551760@qq.com
date:2018/3/19/下午7:14
file:ccc.py
IDE:PyCharm
'''


from django.http import JsonResponse

from kuaishou_admin.models import  Order_combo, Combo_project


def save_taocan_detail(**kwargs):
    """
    创建套餐及其中的数据
    :param kwargs:
    :return:
    """
    print(kwargs)
    taocan_name = kwargs.get("name")
    taocan_gold = kwargs.get("gold")
    taocan_detail = kwargs.get("detail")
    if Order_combo.objects.filter(name=taocan_name).first():
        return {"status": 500, 'msg': 'already exists'}
    taocan = Order_combo.objects.create(name=taocan_name,pro_gold=taocan_gold)
    msg_status = []
    for msg in taocan_detail:

        project = Combo_project.objects.get_or_create(pro_name=msg.get("proName"), count_project=msg.get("num"))
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
    taocan_id = kwargs.get("id")
    taocan_detail = kwargs.get("detail")
    pro_status = []
    taocan = Order_combo.objects.filter(id=taocan_id).first()
    if taocan is None:
        return {"status":500,"msg":"not found "}

    for msg in taocan_detail:
        detail_id = msg.get('project_id')
        print(detail_id)
        proj = Combo_project.objects.filter(id=detail_id).first()
        if proj is not None:
            print("**********")
            taocan.project_detail.remove(proj.id)
            project_new = Combo_project.objects.get_or_create(pro_name=msg.get("proName"), count_project=msg.get("num"))
            taocan.project_detail.add(project_new[0].id)
            pro_status.append(project_new[1])
        else:
            return {"status":500,"msg":"not found "}

    if any(pro_status):
        taocan.name = taocan_name
        taocan.pro_gold = taocan_gold
        taocan.save()
        print(taocan.project_detail.all())
        return {"status":0}
    else:
        return {"status":500,"msg":"update data failed "}



def delete_pro_in_taocan(**kwargs):
    taocan_id = kwargs.get("id")
    project_id = kwargs.get("project_id")
    taocan = Order_combo.objects.filter(id=taocan_id).first()
    if taocan is not None:
        proj_all = taocan.project_detail.all()
        proj = Combo_project.objects.filter(id=project_id).first()
        if proj is not None:
            if proj in proj_all:
                taocan.project_detail.remove(proj.id)
            else:
                return {"status":500,"msg":"this project is not in combo"}
            return {"status":0}
        else:
            return {"status":500,"msg":"project is not exists"}
    else:
        return {"status":500,"msg":"taocan is not exists"}



