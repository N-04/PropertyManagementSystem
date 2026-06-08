from django.urls import path

from apps.finance.views.fee_view import (
    FeeCreateView,
    FeeListView,
    FeeUpdateView,
    FeeDeleteView,
    FeePayView,
)

urlpatterns = [
    path("create/", FeeCreateView.as_view()),
    path("list/", FeeListView.as_view()),
    path(
        "update/<int:pk>/",
        FeeUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        FeeDeleteView.as_view(),
    ),
    path(
        "pay/<int:pk>/",
        FeePayView.as_view(),
    ),
]
