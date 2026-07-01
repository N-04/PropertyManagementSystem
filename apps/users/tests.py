# 文件说明：覆盖用户认证相关的安全回归测试。

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class LogoutRefreshTokenTests(TestCase):
    """退出登录必须让 refresh token 在服务端失效。"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="logout_user",
            password="Wy@Test123",
            status=1,
            is_active=True,
        )

    def test_logout_blacklists_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.force_authenticate(user=self.user)
        logout_response = self.client.post(
            "/api/auth/logout/",
            {"refresh": str(refresh)},
            format="json",
        )

        self.assertEqual(logout_response.status_code, 200)

        self.client.force_authenticate(user=None)
        refresh_response = self.client.post(
            "/api/auth/token/refresh/",
            {"refresh": str(refresh)},
            format="json",
        )

        self.assertEqual(refresh_response.status_code, 401)
