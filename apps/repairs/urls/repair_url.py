from django.urls import path

from apps.repairs.views.repair_view import (
    RepairCreateView,
    RepairListView,
    RepairUpdateView,
    RepairDeleteView,
)

urlpatterns = [
    path(
        "create/",
        RepairCreateView.as_view(),
    ),
    path(
        "list/",
        RepairListView.as_view(),
    ),
    path(
        "update/<int:pk>/",
        RepairUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        RepairDeleteView.as_view(),
    ),
]
