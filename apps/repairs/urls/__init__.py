# 文件说明：声明 Python 包，便于模块被项目导入。

from django.urls import include, path

urlpatterns = [
    path("repair/", include("apps.repairs.urls.repair_url")),
]
