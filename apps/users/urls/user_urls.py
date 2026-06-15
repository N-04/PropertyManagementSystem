# 文件说明：配置 apps/users/urls/user_urls.py 对应业务模块的接口路由。

# 导入视图
from django.urls import path

from apps.users.views.user_view import (
    CurrentUserPasswordView,
    UserAuditView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserInfoView,
    UserListView,
    UserMenusView,
)

urlpatterns = [
    # 创建用户
    path("create/", UserCreateView.as_view()),
    path("menus/", UserMenusView.as_view()),
    path("info/", UserInfoView.as_view()),
    path("profile/", UserInfoView.as_view()),
    path("password/", CurrentUserPasswordView.as_view()),
    # 用户列表
    path("list/", UserListView.as_view()),
    path("delete/<int:pk>/", UserDeleteView.as_view()),
    path("info/<int:pk>/", UserDetailView.as_view()),
    path("audit/<int:pk>/", UserAuditView.as_view()),
]
