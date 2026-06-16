# 文件说明：配置 apps/parking/urls/parking_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.parking.views.parking_view import (
    ParkingCreateView,
    ParkingListView,
    ParkingUpdateView,
    ParkingDeleteView,
    ParkingDetailView,
    ParkingBindView,
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
    path(
        "bind/<int:pk>/",
        ParkingBindView.as_view(),
    ),
]
