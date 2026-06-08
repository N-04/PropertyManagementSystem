from django.urls import path

from apps.logs.views.login_log_view import LoginLogListView
from apps.logs.views.login_log_export_view import LoginLogExportView

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
