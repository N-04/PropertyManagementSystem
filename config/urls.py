from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/auth/',
         include('apps.users.urls.auth_urls')
    ),

    path(
        'api/repair/',
        include('apps.repairs.urls')
    ),

    path(
        'api/permission/',
        include('apps.users.urls.permission_urls')
    ),

    path(
        'api/role/',
        include('apps.users.urls.role_urls')
    ),

    path(
        'api/user/',
        include('apps.users.urls.user_urls')
    ),
    path(
        'api/',
        include('apps.users.urls')
)
]