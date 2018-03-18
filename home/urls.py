from django.conf.urls import url
from home import views
urlpatterns = [
    url(r'^fans$', views.shuafenshi),
    url(r'^home$', views.home),
    url(r'^click$', views.shuangji_page),
    url(r'^combo$', views.remenTaocan),
    url(r'^play$', views.play_home_page),
]