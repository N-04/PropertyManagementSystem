from django.urls import path

from apps.community.views import CommunityCreateView, CommunityListView

urlpatterns = [
    path("create/", CommunityCreateView.as_view()),
    path("list/", CommunityListView.as_view()),
]
