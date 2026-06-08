from django.urls import path, include

urlpatterns = [
    path(
        "",
        include("apps.cars.urls.cars_url"),
    ),
]
