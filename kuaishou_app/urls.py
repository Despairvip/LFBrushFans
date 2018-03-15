from django.conf.urls import url
from kuaishou_app import views

urlpatterns = [
        url(r'^click$', views.ClickView.as_view()),
        url(r'^play$', views.PlayView.as_view()),
        url(r'^fans$', views.FansView.as_view()),
        url(r'^integral$', views.IntegralView.as_view()),
        url(r'^download$', views.DownloadView.as_view()),
        url(r'^center$', views.CenterView.as_view()),
        url(r'^confirm$', views.ConfirmView.as_view()),
        url(r'^notes$', views.NotesView.as_view()),
        url(r'^login$', views.ClientLoginView.as_view()),
        url(r'^pay$', views.PayApi.as_view()),
        url(r'^index$', views.IndexView.as_view()),

]