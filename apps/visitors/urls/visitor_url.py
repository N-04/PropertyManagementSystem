from django.urls import path

from apps.visitors.views.visitor_view import (
    VisitorCreateView,
    VisitorListView,
    VisitorUpdateView,
    VisitorDeleteView,
    VisitorDetailView,
)

urlpatterns = [
    path(
        "list/",
        VisitorListView.as_view(),
    ),
    path(
        "create/",
        VisitorCreateView.as_view(),
    ),
    path(
        "update/<int:pk>/",
        VisitorUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        VisitorDeleteView.as_view(),
    ),
    path(
        "detail/<int:pk>/",
        VisitorDetailView.as_view(),
    ),
]
