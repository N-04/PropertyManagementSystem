from django.urls import path, include

urlpatterns = [
    path(
        "",
        include("apps.dashboard.urls.dashboard_urls"),
    ),
]
