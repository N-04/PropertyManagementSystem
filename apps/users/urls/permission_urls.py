# =====================================================
# 导入 path
# =====================================================

from django.urls import path

# =====================================================
# 导入视图
# =====================================================

from apps.users.views.permission_view import (
    PermissionListView,
    PermissionCreateView,
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
