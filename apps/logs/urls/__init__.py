from django.urls import include
from django.urls import path

urlpatterns = [
    path(
        # 操作日志
        "operation/",
        include("apps.logs.urls.operation_log_url"),
    ),
    # 登录日志
    path(
        "login/",
        include("apps.logs.urls.login_log_url"),
    ),
]
