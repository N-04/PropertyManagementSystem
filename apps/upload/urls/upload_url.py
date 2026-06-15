# 文件说明：配置 apps/upload/urls/upload_url.py 对应业务模块的接口路由。

from django.urls import path

from apps.upload.views.upload_view import (
    UploadView,
)

urlpatterns = [
    path(
        "upload/",
        UploadView.as_view(),
    ),
]
