# 文件说明：配置 apps/repairs/urls/repair_url.py 对应业务模块的接口路由。

from django.urls import path

from apps.repairs.views.repair_view import (
    RepairCreateView,
    RepairListView,
    RepairUpdateView,
    RepairDeleteView,
    RepairDetailView,
    RepairAssignView,
)

urlpatterns = [
    path(
        "create/",
        RepairCreateView.as_view(),
    ),
    path(
        "list/",
        RepairListView.as_view(),
    ),
    path(
        "update/<int:pk>/",
        RepairUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        RepairDeleteView.as_view(),
    ),
    path(
        "detail/<int:pk>/",
        RepairDetailView.as_view(),
    ),
    path(
        "assign/<int:pk>/",
        RepairAssignView.as_view(),
    ),
]
