from django.urls import path, include

urlpatterns = [
    path(
        "",
        include("apps.finance.urls.fee_urls"),
    ),
]
