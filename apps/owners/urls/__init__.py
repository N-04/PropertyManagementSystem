from django.urls import path, include

urlpatterns = [
    path(
        "",
        include("apps.owners.urls.owner_urls"),
    ),
]
