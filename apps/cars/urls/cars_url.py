from django.urls import path

from apps.cars.views import (
    CarCreateView,
    CarListView,
    CarUpdateView,
    CarDeleteView,
    CarDetailView,
)

urlpatterns = [
    # 新增车辆
    path(
        "create/",
        CarCreateView.as_view(),
    ),
    # 车辆列表
    path(
        "list/",
        CarListView.as_view(),
    ),
    # 修改车辆
    path(
        "update/<int:pk>/",
        CarUpdateView.as_view(),
    ),
    # 删除车辆
    path(
        "delete/<int:pk>/",
        CarDeleteView.as_view(),
    ),
    path("detail/<int:pk>/", CarDetailView.as_view()),
]
