# 文件说明：配置 apps/logs/urls/login_log_url.py 对应业务模块的接口路由。

from django.urls import path

from apps.logs.views.login_log_export_view import LoginLogExportView
from apps.logs.views.login_log_view import LoginLogListView

urlpatterns = [
    # 登录日志列表
    path(
        "list/",
        LoginLogListView.as_view(),
    ),
    # 登录日志导出
    path(
        "export/",
        LoginLogExportView.as_view(),
    ),
]
