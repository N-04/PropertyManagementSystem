from django.urls import path, include

urlpatterns = [

    path(
        'menu/',
        include('apps.users.urls.menu_urls')
    ),

]