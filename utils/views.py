import datetime
import random


def createOrdernumber(user_id, project_id):
    _date = datetime.datetime.now()
    ordernumber_1 = datetime.datetime.strftime(_date, '%Y%m%d%H%M%S')
    f = datetime.datetime.strftime(_date, '%f')
    ordernumber_2 = ""

    ordernumber_2 += random.choice("123456789")
    ordernumber_2 += "0" * (3 - len(str(user_id))) + str(user_id)[0:3]
    ordernumber_2 += "0" * (3 - len(str(project_id))) + str(project_id)[0:3]

    ordernumber_2 += "0" * (3 - len(f)) + f[0:3]
    #     zj = project.gold *count
    ordernumber_2 += "".join([random.choice("0123456789") for j in range(0, 2)])
    return "%s%s"%(ordernumber_1, ordernumber_2)

