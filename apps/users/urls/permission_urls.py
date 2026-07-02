# 文件说明：配置 apps/users/urls/permission_urls.py 对应业务模块的接口路由。

# =====================================================
# 导入 path
# =====================================================

from django.urls import path

# =====================================================
# 导入视图
# =====================================================
from apps.users.views.permission_view import (
    PermissionCreateView,
    PermissionListView,
    PermissionTreeView,
)

urlpatterns = [
    # =================================================
    # 权限列表
    # =================================================
    path("list/", PermissionListView.as_view()),
    # =================================================
    # 权限新增
    # =================================================
    path("create/", PermissionCreateView.as_view()),
    # 权限树
    path("tree/", PermissionTreeView.as_view()),
]
