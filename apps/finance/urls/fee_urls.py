# 文件说明：配置 apps/finance/urls/fee_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.finance.views.fee_view import (
    FeeCreateView,
    FeeListView,
    FeeUpdateView,
    FeeDeleteView,
    FeePayView,
    FeeReminderView,
)

urlpatterns = [
    path("create/", FeeCreateView.as_view()),
    path("list/", FeeListView.as_view()),
    path(
        "update/<int:pk>/",
        FeeUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        FeeDeleteView.as_view(),
    ),
    path(
        "pay/<int:pk>/",
        FeePayView.as_view(),
    ),
    path(
        "remind/<int:pk>/",
        FeeReminderView.as_view(),
    ),
]
