from django.urls import path, include
from apps.users.views.permission_view import *


urlpatterns = [

    path(
        'list/',
        PermissionListView.as_view()
    ),
    path(
        'create/',
        PermissionCreateView.as_view()
    ),

    path(
        'detail/<int:pk>/',
        PermissionDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        PermissionUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        PermissionDeleteView.as_view()
    ),
]