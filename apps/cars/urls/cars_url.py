# 文件说明：配置 apps/cars/urls/cars_url.py 对应业务模块的接口路由。

from django.urls import path

from apps.cars.views import (
    CarCreateView,
    CarListView,
    CarUpdateView,
    CarDeleteView,
    CarDetailView,
    CarDisableView,
    CarEnableView,
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
    # 车辆详情
    path("detail/<int:pk>/", CarDetailView.as_view()),
    # 禁用车辆
    path("disable/<int:pk>/", CarDisableView.as_view()),
    # 启用车辆
    path("enable/<int:pk>/", CarEnableView.as_view()),
]
