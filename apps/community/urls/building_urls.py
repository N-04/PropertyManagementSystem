from django.urls import path

from apps.community.views.building_view import BuildingCreateView, BuildingListView

urlpatterns = [
    path("create/", BuildingCreateView.as_view()),
    path("list/", BuildingListView.as_view()),
]
