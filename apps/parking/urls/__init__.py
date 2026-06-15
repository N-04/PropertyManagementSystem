# 文件说明：声明 Python 包，便于模块被项目导入。

from django.urls import path, include

urlpatterns = [
    path("parking/", include("apps.parking.urls.parking_urls")),
]
