from django.http import JsonResponse

from kuaishou_admin.models import  Order_combo, Combo_project


def taocan_save(taocan_name,taocan_gold,projectOneName, projectOneNum, projectTwoName, projectTwoNum, projectThreeName, projectThreeNum):
    projectOne = Combo_project.objects.get_or_create(pro_name=projectOneName, count_project=projectOneNum)
    projectTwo = Combo_project.objects.get_or_create(pro_name=projectTwoName, count_project=projectTwoNum)
    projectThree = Combo_project.objects.get_or_create(pro_name=projectThreeName, count_project=projectThreeNum)
    print(projectOne,projectTwo,projectThree)

    if projectOne[1] or projectTwo[1] or projectThree[1]:
        taocan = Order_combo.objects.create(name=taocan_name, pro_gold=taocan_gold)
        taocan.project_detail.add(projectOne[0], projectTwo[0], projectThree[0])
        taocan.save()
        return True
    else:
        return False


def update_taocan_msg(taocan_name,taocan_gold,taocan,
                      projectOneName, projectOneNum, projectOneid,
                      projectTwoName, projectTwoNum, projectTwoid,
                      projectThreeName, projectThreeNum, projectThreeid):
    projectOne = Combo_project.objects.filter(id=projectOneid).first()
    if projectOne is None:
        return {"status": 500, "msg": "project not exists"}

    projectOne_new = Combo_project.objects.get_or_create(pro_name=projectOneName, count_project=projectOneNum)
    if projectOne_new[1]:
        taocan.project_detail.remove(projectOne.id)
        taocan.project_detail.add(projectOne_new[0].id)

    projectTwo = Combo_project.objects.filter(id=projectTwoid).first()
    if projectTwo is None:
        return {"status": 500, "msg": "project not exists"}

    projectTwo_new = Combo_project.objects.get_or_create(pro_name=projectTwoName, count_project=projectTwoNum)

    if projectTwo_new[1]:
        taocan.project_detail.remove(projectTwo.id)
        taocan.project_detail.add(projectTwo_new[0].id)


    projectThree = Combo_project.objects.filter(id=projectThreeid).first()
    if projectThree is None:
        return {"status": 500, "msg": "project not exists"}


    projectThree_new = Combo_project.objects.get_or_create(pro_name=projectThreeName, count_project=projectThreeNum)

    if projectThree_new[1]:
        taocan.project_detail.remove(projectThree.id)
        taocan.project_detail.add(projectThree_new[0].id)




    if projectOne_new[1] or projectTwo_new[1] or projectThree_new[1]:
        taocan.name = taocan_name
        taocan.pro_gold = taocan_gold
        taocan.save()
        print(taocan.project_detail.all())
        return {"status":0}
    else:
        return {"status":500,"msg":"you don't change these projects"}
