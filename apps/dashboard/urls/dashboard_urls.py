from django.urls import path

from apps.dashboard.views.dashboard_view import DashboardView

urlpatterns = [
    # 首页统计接口
    path(
        "",
        DashboardView.as_view(),
    ),
]
