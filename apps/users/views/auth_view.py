# 文件说明：处理 apps/users/views/auth_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.logs.models.login_log import LoginLog
from apps.users.models.user import User
from apps.users.serializers.auth_serializer import (
    LogoutSerializer,
    PasswordLoginSerializer,
    PasswordResetSerializer,
    PhoneLoginSerializer,
    RegisterSerializer,
    SmsCodeSerializer,
)
from apps.users.utils.captcha import create_captcha
from apps.users.utils.sms import SMS_COOLDOWN, SMS_TTL, create_sms_code
from common.response.response import ResponseError, ResponseSuccess


def _build_token_data(user):
    """
    统一生成登录成功后的 JWT 返回数据。

    access token 给前端放在 Authorization 里访问接口；
    refresh token 用于后续刷新 token 或退出登录时加入黑名单。
    """
    refresh = RefreshToken.for_user(user)
    role_codes = list(user.roles.values_list("code", flat=True))

    if user.role_id and user.role.code not in role_codes:
        role_codes.insert(0, user.role.code)

    if user.is_superuser and not role_codes:
        role_codes = ["super_admin"]

    return {
        "token": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username,
        "phone": user.phone,
        "role": role_codes[0] if role_codes else "",
        "roles": role_codes,
    }


def _ensure_user_can_login(user):
    """
    登录前的账号状态校验。

    超级管理员优先放行，避免业务状态字段影响 Django 后台管理账号。
    普通用户需要同时满足 is_active=True 和 status=1。
    """
    if not user:
        return "账号不存在或密码错误"

    if user.is_superuser:
        return None

    if not user.is_active or user.status != 1:
        return "账号已被禁用"

    return None


class CaptchaView(APIView):
    """
    图形验证码接口。

    不需要登录，前端进入登录/注册/发送短信验证码页面时调用。
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # 返回 captcha_key 和 base64 SVG 图片，后续校验时用 captcha_key 找缓存。
        return ResponseSuccess(data=create_captcha(), msg="获取成功")


class SmsCodeView(APIView):
    """
    短信验证码接口。

    purpose 用于区分业务场景：
    register 注册、reset_password 找回密码、login 手机号登录。
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Serializer 会先校验手机号、图形验证码、发送场景是否合法。
        serializer = SmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        purpose = serializer.validated_data["purpose"]
        code = create_sms_code(phone, purpose)

        if not code:
            # 同一个手机号同一场景 60 秒内不能重复发送。
            return ResponseError(msg="验证码已发送，请60秒后再试", code=429)

        data = {
            "expire_seconds": SMS_TTL,
            "cooldown_seconds": SMS_COOLDOWN,
        }

        if settings.DEBUG:
            # 开发环境没有真实短信通道，返回 debug_code 方便本地联调。
            data["debug_code"] = code

        return ResponseSuccess(data=data, msg="短信验证码已发送")


class LoginView(APIView):
    """
    密码登录接口。

    兼容 username + password 和 phone + password 两种登录方式。
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]
        password = serializer.validated_data["password"]

        # identifier 可能是手机号，也可能是用户名；先按手机号查，查不到再按用户名查。
        user = User.objects.filter(phone=identifier).first()

        if not user:
            user = User.objects.filter(username=identifier).first()

        login_error = _ensure_user_can_login(user)

        if login_error:
            return ResponseError(msg=login_error)

        # Django 的 authenticate 仍然用 username 字段验证密码。
        auth_user = authenticate(username=user.username, password=password)

        if not auth_user:
            return ResponseError(msg="账号不存在或密码错误")

        # 密码验证成功后再记录登录日志，避免失败密码也被记成成功登录。
        LoginLog.objects.create(
            username=auth_user.username,
            ip=request.META.get("REMOTE_ADDR"),
        )

        return ResponseSuccess(data=_build_token_data(auth_user), msg="登录成功")


class PhoneLoginView(APIView):
    """
    手机号验证码登录接口。

    验证短信验证码后直接给用户签发 JWT。
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PhoneLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(phone=serializer.validated_data["phone"]).first()
        login_error = _ensure_user_can_login(user)

        if login_error:
            return ResponseError(msg=login_error)

        LoginLog.objects.create(
            username=user.username,
            ip=request.META.get("REMOTE_ADDR"),
        )

        return ResponseSuccess(data=_build_token_data(user), msg="登录成功")


class RegisterView(APIView):
    """
    注册接口。

    当前不新增注册审核表字段，注册用户默认 is_active=False、status=0；
    管理员审核通过时调用用户审核接口启用账号。
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseError(
                msg="注册失败",
                data=serializer.errors,
            )

        user = serializer.save()

        return ResponseSuccess(
            msg="注册成功，请等待管理员审核",
            data={
                "id": user.id,
                "phone": user.phone,
            },
        )


class PasswordResetView(APIView):
    """
    找回密码接口。

    使用手机号 + 短信验证码确认身份，然后重置密码。
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResponseSuccess(msg="密码重置成功")


class LogoutView(APIView):
    """
    退出登录接口。

    如果项目启用了 SimpleJWT blacklist，会尝试把 refresh token 加入黑名单；
    没启用 blacklist 时也正常返回成功，由前端清理本地 token。
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")

        if refresh_token:
            try:
                # token_blacklist 未安装时 blacklist 方法不可用，所以这里兼容处理。
                RefreshToken(refresh_token).blacklist()
            except AttributeError:
                pass
            except Exception:
                pass

        return ResponseSuccess(msg="退出登录成功")
