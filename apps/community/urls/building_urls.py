# 文件说明：配置 apps/community/urls/building_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.community.views.building_view import BuildingCreateView, BuildingListView

urlpatterns = [
    path("create/", BuildingCreateView.as_view()),
    path("list/", BuildingListView.as_view()),
]
