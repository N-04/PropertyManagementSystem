from django.urls import path

from apps.notice.views import (
    NoticeCreateView,
    NoticeListView,
    NoticeUpdateView,
    NoticeDeleteView,
    NoticeDetailView,
)

urlpatterns = [
    path("create/", NoticeCreateView.as_view()),
    path("list/", NoticeListView.as_view()),
    path(
        "update/<int:pk>/",
        NoticeUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        NoticeDeleteView.as_view(),
    ),
    path(
        "detail/<int:pk>/",
        NoticeDetailView.as_view(),
    ),
]
