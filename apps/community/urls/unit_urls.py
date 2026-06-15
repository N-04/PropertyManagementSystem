# 文件说明：配置 apps/community/urls/unit_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.community.views.unit_view import UnitCreateView, UnitListView

urlpatterns = [
    path("create/", UnitCreateView.as_view()),
    path("list/", UnitListView.as_view()),
]
