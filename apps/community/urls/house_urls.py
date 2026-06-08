from django.urls import path

from apps.community.views.house_view import (
    HouseCreateView,
    HouseListView,
    HouseUpdateView,
    HouseDeleteView,
)

urlpatterns = [
    path(
        "create/",
        HouseCreateView.as_view(),
    ),
    path(
        "list/",
        HouseListView.as_view(),
    ),
    path("update/<int:pk>/", HouseUpdateView.as_view()),
    path("delete/<int:pk>/", HouseDeleteView.as_view()),
]
