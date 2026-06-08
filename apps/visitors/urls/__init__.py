from django.urls import path, include

urlpatterns = [
    path("visitor/", include("apps.visitors.urls.visitor_url")),
]
