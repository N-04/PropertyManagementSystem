from django.urls import path

from apps.parking.views.parking_view import (
    ParkingCreateView,
    ParkingListView,
    ParkingUpdateView,
    ParkingDeleteView,
    ParkingDetailView,
)

urlpatterns = [
    path(
        "create/",
        ParkingCreateView.as_view(),
    ),
    path(
        "list/",
        ParkingListView.as_view(),
    ),
    path(
        "update/<int:pk>/",
        ParkingUpdateView.as_view(),
    ),
    path(
        "delete/<int:pk>/",
        ParkingDeleteView.as_view(),
    ),
    path(
        "detail/<int:pk>/",
        ParkingDetailView.as_view(),
    ),
]
