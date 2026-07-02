# 文件说明：配置 apps/parking/urls/parking_urls.py 对应业务模块的接口路由。

from django.urls import path

from apps.parking.views.parking_view import (
    ParkingBindView,
    ParkingCreateView,
    ParkingDeleteView,
    ParkingDetailView,
    ParkingListView,
    ParkingUpdateView,
)

urlpatterns = [
    # 管理端维护车位基础信息。
    path(
        "create/",
        ParkingCreateView.as_view(),
    ),
    # 车位列表按角色返回我的车位、可购买车位或管理端全量数据。
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
    # 绑定接口用于业主购买/绑定车位后的归属更新。
    path(
        "bind/<int:pk>/",
        ParkingBindView.as_view(),
    ),
]
