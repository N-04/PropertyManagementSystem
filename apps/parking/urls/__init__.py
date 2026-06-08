from django.urls import path, include

urlpatterns = [
    path("parking/", include("apps.parking.urls.parking_urls")),
]
