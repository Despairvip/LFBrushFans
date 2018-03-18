"""
Django settings for Demo project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7y-sf9t=k3#-hn*=62%1vgyxmjxn&rsx%9(s05vquz0m6&nm@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = True # 通过这种方式可以打开 DEBUG 模式
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
                'format': '%(levelname)s %(asctime)s %(message)s'
                },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'test1_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(BASE_DIR,'utils/log/app_log.log').replace('\\','/'),
            'formatter':'standard',
        },
        'test2_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(BASE_DIR,'utils/log/admin_log.log').replace('\\','/'),
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_app':{
            'handlers': ['test1_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'django_admin':{
            'handlers': ['test2_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_WHITELIST = (
      '*',
)


INSTALLED_APPS = (
    'corsheaders',##
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kuaishou_admin',
    'kuaishou_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',##
    'django.middleware.common.CommonMiddleware',##
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+"/templates",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LFBrushFans',
        'USER':'root',
        'PASSWORD':'mysql',
        'HOST':'127.0.0.1',
        'PORT':'3306'
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.211.55.5:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Session

# SESSION_ENGINE = "django.contrib.sessions.backends.db"


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# alipay
ALIPAY_APPID = 	"2016091100488045"

AUTH_USER_MODEL = 'kuaishou_admin.Client'

LOGIN_URL = "/login/"

# alipay
ALIPAY_APPID = 	" 2018011601908317"
# 微信登录
APP_ID = 'wxd3548103f87244c4'
SECRET_APP = 'af4992a76cca43e9ec0f2bfd6205fe6c'