from sfpt.settings_base import *


DEBUG = True

import pymysql

pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sfpt',
        'USER': 'sfpt',
        'PASSWORD':"82D6X2ud369",
        'HOST':'rm-uf6476u9lp566f39t.mysql.rds.aliyuncs.com',
        'PORT':'3306',
        'OPTIONS':{
            "charset": "utf8mb4",
        }
    },
}

STATIC_URL = 'http://ksht-static.3agzs.com/'
STATIC_ROOT = os.path.join(BASE_DIR,'/static/').replace('\\','/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

