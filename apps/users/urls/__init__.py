from django.urls import path, include
from .menu_urls import urlpatterns as menu_urlpatterns

urlpatterns = [

    path(
        'menu/',
        include('apps.users.urls.menu_urls')
    ),

]