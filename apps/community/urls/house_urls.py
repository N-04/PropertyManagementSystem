# 文件说明：配置 apps/community/urls/house_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.community.views.house_view import (
    HouseCreateView,
    HouseListView,
    HouseUpdateView,
    HouseDeleteView,
)

urlpatterns = [
    path(
        "create/",
        HouseCreateView.as_view(),
    ),
    path(
        "list/",
        HouseListView.as_view(),
    ),
    path("update/<int:pk>/", HouseUpdateView.as_view()),
    path("delete/<int:pk>/", HouseDeleteView.as_view()),
]
