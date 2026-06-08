from django.urls import path, include

urlpatterns = [
    path("repair/", include("apps.repairs.urls.repair_url")),
]
