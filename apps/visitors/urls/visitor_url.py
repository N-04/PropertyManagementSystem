# 文件说明：配置 apps/visitors/urls/visitor_url.py 对应业务模块的接口路由。

from django.urls import path

from apps.visitors.views.visitor_view import (
    VisitorApproveView,
    VisitorCreateView,
    VisitorDeleteView,
    VisitorDetailView,
    VisitorEnterView,
    VisitorLeaveView,
    VisitorListView,
    VisitorUpdateView,
)

urlpatterns = [
    path(
        "list/",
        VisitorListView.as_view(),
    ),
    path(
        "create/",
        VisitorCreateView.as_view(),
    ),
    path(
        "update/<int:pk>/",
        VisitorUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        VisitorDeleteView.as_view(),
    ),
    path(
        "detail/<int:pk>/",
        VisitorDetailView.as_view(),
    ),
    path(
        "approve/<int:pk>/",
        VisitorApproveView.as_view(),
    ),
    path(
        "enter/<int:pk>/",
        VisitorEnterView.as_view(),
    ),
    path(
        "leave/<int:pk>/",
        VisitorLeaveView.as_view(),
    ),
]
