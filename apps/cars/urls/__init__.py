# 文件说明：声明 Python 包，便于模块被项目导入。

from django.urls import path, include

urlpatterns = [
    path(
        "",
        include("apps.cars.urls.cars_url"),
    ),
]
