from sfpt.settings_base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sfpttest',
        'USER': 'sfpttest',
        'PASSWORD': "a4P7W24i772",
        'HOST': 'rm-uf6476u9lp566f39t.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'OPTIONS': {
            "charset": "utf8mb4",
        }
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/').replace('\\', '/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


