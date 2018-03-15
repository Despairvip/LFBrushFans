from django.conf.urls import url
from kuaishou_admin import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view, name="login"),
    url(r'^logout$', views.LogoutView.as_view, name="logout"),
    url(r'^orders$', views.RealOrdersView.as_view, name="orders"),
    url(r'^search$', views.OptionSearchView.as_view, name="search"),
    url(r'^idsearch$', views.EnterSearchView.as_view, name="idsearch"),
    url(r'^usersearch$', views.UserSearchView.as_view, name="usersearch"),
    url(r'^change$', views.ModifyStatusView.as_view, name="change"),
    url(r'^edit$', views.ModifyGoldView.as_view, name="edit"),
    url(r'^users$', views.UserListView.as_view, name="usersearch"),


]

