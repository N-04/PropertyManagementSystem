# 文件说明：配置 apps/dashboard/urls/dashboard_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.dashboard.views.dashboard_view import DashboardView, VisitorStatisticsView

urlpatterns = [
    # 首页统计接口
    path(
        "",
        DashboardView.as_view(),
    ),
    path(
        "statistics/",
        VisitorStatisticsView.as_view(),
    ),
]
