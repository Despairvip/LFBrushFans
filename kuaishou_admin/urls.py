from django.conf.urls import url
from kuaishou_admin import views

''' Despair modified'''
urlpatterns = [
    # url(r'^login$', views.LoginView, name="login"),  # 登陆
    url(r'^logout$', views.LogoutView, name="logout"),  # 退出
    url(r'^orders$', views.RealOrdersView, name="orders"),  # 实时订单(废弃)
    url(r'^search$', views.OptionSearchView, name="search"),  # 下拉框搜索
    url(r'^idsearch$', views.EnterSearchView, name="idsearch"),  # 根据订单号查询订单
    url(r'^usersearch$', views.UserSearchView, name="usersearch"),  # 根据用户id查询订单
    url(r'^change$', views.ModifyStatusView, name="change"),  # 修改订单状态
    url(r'^edit$', views.ModifyGoldView, name="edit"),  # 修改金币
    url(r'^users$', views.UserListView, name="usersearch"),  # 用户列表
    url(r'^add$', views.add_wechat),  # 添加客服微信号
    url(r'^update$', views.new_version_update),  # 用户版本更新
    url(r'^all$', views.all_project),  # 用户版本更新
    url(r'^combo$', views.all_project),  # 套餐

]
