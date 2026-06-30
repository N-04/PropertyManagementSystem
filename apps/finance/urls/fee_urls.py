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
    # 财务人员创建账单，业主端仅消费列表和支付接口。
    path("create/", FeeCreateView.as_view()),
    # 账单列表同时服务财务筛选、业主在线缴费和缴费记录。
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
    # 欠费提醒只发送消息通知，不跳转欠费列表。
    path(
        "remind/<int:pk>/",
        FeeReminderView.as_view(),
    ),
]
