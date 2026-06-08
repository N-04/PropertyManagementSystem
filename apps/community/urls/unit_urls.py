from django.urls import path

from apps.community.views.unit_view import UnitCreateView, UnitListView

urlpatterns = [
    path("create/", UnitCreateView.as_view()),
    path("list/", UnitListView.as_view()),
]
