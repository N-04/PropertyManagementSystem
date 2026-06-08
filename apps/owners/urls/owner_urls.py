from django.urls import path

from apps.owners.views.owner_view import (
    OwnerCreateView,
    OwnerListView,
    OwnerUpdateView,
    OwnerDeleteView,
    OwnerDetailView,
)

urlpatterns = [
    path(
        "create/",
        OwnerCreateView.as_view(),
    ),
    path(
        "list/",
        OwnerListView.as_view(),
    ),
    path("update/<int:pk>/", OwnerUpdateView.as_view()),
    path("delete/<int:pk>/", OwnerDeleteView.as_view()),
    path("detail/<int:pk>/", OwnerDetailView.as_view()),
]
