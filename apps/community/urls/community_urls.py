# 文件说明：配置 apps/community/urls/community_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.community.views import CommunityCreateView, CommunityListView

urlpatterns = [
    path("create/", CommunityCreateView.as_view()),
    path("list/", CommunityListView.as_view()),
]
