from django.urls import path

from apps.users.views.role_view import *

urlpatterns = [

    path(
        'create/',
        RoleCreateView.as_view()
    ),

    path(
        'list/',
        RoleListView.as_view()
    ),

    path(
        'detail/<int:pk>/',
        RoleDetailView.as_view()
    ),
    path(
        'update/<int:pk>/',
        RoleUpdateView.as_view()
    )
]