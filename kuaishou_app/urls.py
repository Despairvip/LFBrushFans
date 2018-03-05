from django.conf.urls import url
from kuaishou_app import views

urlpatterns = [
        url(r'^index$', views.IndexView.as_view()),
        url(r'^click$', views.ClickView.as_view()),
        url(r'^play$', views.PlayView.as_view()),
        url(r'^download$', views.DownloadView.as_view()),
        url(r'^fans$', views.FansView.as_view()),
        url(r'^integral$', views.IntegralView.as_view()),
        url(r'^number$', views.NumberView.as_view()),
        url(r'^center$', views.CenterView.as_view()),
        url(r'^package$', views.PackageView.as_view()),
        url(r'^confirm$', views.ConfirmView.as_view()),
        url(r'^notes$', views.NotesView.as_view()),
        url(r'^news$', views.NotesView.as_view()),

]