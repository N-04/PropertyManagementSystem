# 文件说明：声明 Python 包，便于模块被项目导入。

from django.urls import include, path

urlpatterns = [
    path("community/", include("apps.community.urls.community_urls")),
    path("building/", include("apps.community.urls.building_urls")),
    path("unit/", include("apps.community.urls.unit_urls")),
    path(
        "house/",
        include("apps.community.urls.house_urls"),
    ),
]
