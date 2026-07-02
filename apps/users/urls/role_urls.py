# 文件说明：配置 apps/users/urls/role_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.users.views.role_view import (
    RoleCreateView,
    RoleDeleteView,
    RoleDetailView,
    RoleListView,
    RolePermissionAssignView,
    RoleUpdateView,
)

urlpatterns = [
    # =====================================================
    # 新增角色
    # =====================================================
    path("create/", RoleCreateView.as_view()),
    path("list/", RoleListView.as_view()),
    path("info/<int:pk>/", RoleDetailView.as_view()),
    # 编辑角色
    path("update/<int:pk>/", RoleUpdateView.as_view()),
    # 删除角色
    path("delete/<int:pk>/", RoleDeleteView.as_view()),
    path("assign_permission/", RolePermissionAssignView.as_view()),
]
