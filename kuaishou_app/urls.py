from django.conf.urls import url
from kuaishou_app import views

urlpatterns = [
        url(r'^click$', views.ClickView),
        url(r'^play$', views.PlayView),
        url(r'^fans$', views.FansView),
        url(r'^integral$', views.IntegralView),
        url(r'^download$', views.DownloadView),
        url(r'^center$', views.CenterView),
        url(r'^confirm$', views.ConfirmView),
        url(r'^notes$', views.NotesView),
        url(r'^login$', views.ClientLoginView),
        url(r'^pay$', views.PayApi),
]