from django.conf.urls import url
from kuaishou_admin import views

urlpatterns = [
    # url(r'^login$', views.LoginView, name="login"),
    url(r'^logout$', views.LogoutView, name="logout"),
    url(r'^orders$', views.RealOrdersView, name="orders"),
    url(r'^search$', views.OptionSearchView, name="search"),
    url(r'^idsearch$', views.EnterSearchView, name="idsearch"),
    url(r'^usersearch$', views.UserSearchView, name="usersearch"),
    url(r'^change$', views.ModifyStatusView, name="change"),
    url(r'^edit$', views.ModifyGoldView, name="edit"),
    url(r'^users$', views.UserListView, name="usersearch"),
    url(r'^add$', views.add_wechat),

]

