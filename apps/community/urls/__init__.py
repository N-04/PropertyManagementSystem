from django.urls import path, include

urlpatterns = [
    path("", include("apps.community.urls.community_urls")),
    path("community/", include("apps.community.urls.community_urls")),
    path("building/", include("apps.community.urls.building_urls")),
    path("unit/", include("apps.community.urls.unit_urls")),
    path(
        "house/",
        include("apps.community.urls.house_urls"),
    ),
]
