from django.http import JsonResponse

from kuaishou_admin.models import Project


def taocan_save(projectOneName, projectOneNum, projectTwoName, projectTwoNum, projectThreeName, projectThreeNum):
    projectOne = Project.objects.get_or_create(pro_name=projectOneName, count_project=projectOneNum)
    projectTwo = Project.objects.get_or_create(pro_name=projectTwoName, count_project=projectTwoNum)
    projectThree = Project.objects.get_or_create(pro_name=projectThreeName, count_project=projectThreeNum)

    if projectOne and projectTwo and projectThree:
        return projectOne,projectTwo,projectThree
    else:
        return JsonResponse({"status":500,'msg':'create project error'})


def update_taocan_msg(projectOneName, projectOneNum, projectOneid,
                      projectTwoName, projectTwoNum, projectTwoid,
                      projectThreeName, projectThreeNum, projectThreeid):
    projectOne = Project.objects.filter(id=projectOneid).first()
    if projectOne is None:
        return {"status": 500, "msg": "project not exists"}
    projectOne.pro_name = projectOneName
    projectOne.count_project = projectOneNum
    projectOne.save()

    projectTwo = Project.objects.filter(id=projectTwoid).first()
    if projectOne is None:
        return {"status": 500, "msg": "project not exists"}
    projectTwo.pro_name = projectTwoName
    projectTwo.count_project = projectTwoNum
    projectTwo.save()

    projectThree = Project.objects.filter(id=projectThreeid).first()
    if projectThree is None:
        return {"status": 500, "msg": "project not exists"}
    projectThree.pro_name = projectThreeName
    projectThree.count_project = projectThreeNum
    projectThree.save()

    return projectOne, projectTwo, projectThree
