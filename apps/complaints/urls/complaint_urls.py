# 文件说明：配置投诉建议模块接口路由。
from django.urls import path

from apps.complaints.views import (
    ComplaintCreateView,
    ComplaintDeleteView,
    ComplaintDetailView,
    ComplaintListView,
    ComplaintUpdateView,
)

urlpatterns = [
    path("list/", ComplaintListView.as_view()),
    path("create/", ComplaintCreateView.as_view()),
    path("detail/<int:pk>/", ComplaintDetailView.as_view()),
    path("update/<int:pk>/", ComplaintUpdateView.as_view()),
    path("delete/<int:pk>/", ComplaintDeleteView.as_view()),
]
