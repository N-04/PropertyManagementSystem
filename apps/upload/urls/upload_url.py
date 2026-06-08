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
