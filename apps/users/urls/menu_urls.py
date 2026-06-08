from django.urls import path
from apps.users.views.menu_view import *

urlpatterns = [
    path("create/", MenuCreateView.as_view()),
    path("list/", MenuListView.as_view()),
    path("tree/", MenuTreeView.as_view()),
    path("", MenuTreeView.as_view()),
    path("user_tree/", UserMenuTreeView.as_view()),
]
