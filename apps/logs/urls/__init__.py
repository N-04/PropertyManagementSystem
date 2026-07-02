# 文件说明：声明 Python 包，便于模块被项目导入。

from django.urls import include, path

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
