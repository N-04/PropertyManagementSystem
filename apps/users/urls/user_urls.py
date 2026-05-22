from django.urls import path

from apps.users.views.user_view import *

urlpatterns = [

    path(
        'create/',
        UserCreateView.as_view()
    ),
    path(
        'menus/',
        UserMenusView.as_view()
    )
]