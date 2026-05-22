from django.urls import path

from apps.users.views.auth_view import LoginView
from apps.users.views.user_view import UserInfoView


urlpatterns = [
    path('login/', LoginView.as_view()),

    path('userinfo/', UserInfoView.as_view()),
]