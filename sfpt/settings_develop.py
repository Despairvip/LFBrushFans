from sfpt.settings_base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
import pymysql

pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LFBrushFans',
        'USER': 'root',
        'PASSWORD':"",
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            "charset": "utf8mb4",
        }

    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/').replace('\\', '/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


'''
django_debug_toolbar 配置

'''


# DEBUG_TOOLBAR_PATCH_SETTINGS = False
#
# INSTALLED_APPS = INSTALLED_APPS + (
#     'debug_toolbar', 'pympler'
#
# )
#
#
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'pympler.panels.MemoryPanel',
# ]
#
# MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
#
# INTERNAL_IPS = ("127.0.0.1",)