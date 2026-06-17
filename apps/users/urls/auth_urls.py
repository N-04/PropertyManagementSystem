# 文件说明：配置 apps/users/urls/auth_urls.py 对应业务模块的接口路由。

# 导入 path
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# 导入 view
from apps.users.views.auth_view import (
    CaptchaView,
    LoginView,
    LogoutView,
    PasswordResetView,
    PhoneLoginView,
    RegisterView,
    SmsCodeView,
)
from apps.users.views.user_view import UserInfoView

urlpatterns = [
    # 图形验证码
    path("captcha/", CaptchaView.as_view()),

    # 短信验证码
    path("sms-code/", SmsCodeView.as_view()),

    # 登录接口
    path("login/", LoginView.as_view()),

    # 刷新 access token，避免用户登录一段时间后访问列表接口直接 401。
    path("token/refresh/", TokenRefreshView.as_view()),

    # 手机号验证码登录
    path("login/phone/", PhoneLoginView.as_view()),

    # 退出登录
    path("logout/", LogoutView.as_view()),

    # 注册
    path("register/", RegisterView.as_view()),

    # 找回密码
    path("password/reset/", PasswordResetView.as_view()),

    # 当前用户信息
    path("userinfo/", UserInfoView.as_view()),
]
