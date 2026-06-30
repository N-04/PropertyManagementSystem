# 文件说明：配置 apps/upload/urls/upload_url.py 对应业务模块的接口路由。

from django.urls import path

from apps.upload.views.upload_view import (
    UploadView,
)

urlpatterns = [
    # 通用文件上传入口，按 type 区分头像、身份证、报修图片等业务场景。
    path(
        "upload/",
        UploadView.as_view(),
    ),
]
