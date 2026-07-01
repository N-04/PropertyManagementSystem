# 文件说明：负责 apps/users/serializers/auth_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.users.models.user import User
from apps.users.utils.captcha import validate_captcha
from apps.users.utils.sms import SMS_PURPOSES, validate_sms_code
from apps.users.utils.validators import (
    validate_id_card,
    validate_password_strength,
    validate_phone_format,
)


class PasswordLoginSerializer(serializers.Serializer):
    """
    密码登录参数校验。

    支持用户名登录，也支持手机号登录；密码登录必须校验图形验证码，
    防止绕过验证码直接撞库。
    """

    username = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField()
    captcha_key = serializers.CharField(required=False, allow_blank=True)
    captcha_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        username = attrs.get("username")
        phone = attrs.get("phone")

        # 统一把用户名或手机号收敛成 identifier，视图层就不用关心登录类型。
        if phone:
            validate_phone_format(phone)
            attrs["identifier"] = phone
        elif username:
            attrs["identifier"] = username
        else:
            raise serializers.ValidationError("用户名或手机号不能为空")

        captcha_key = attrs.get("captcha_key")
        captcha_code = attrs.get("captcha_code")

        if not captcha_key or not captcha_code:
            raise serializers.ValidationError("图形验证码不能为空")

        if not validate_captcha(captcha_key, captcha_code):
            raise serializers.ValidationError("图形验证码错误或已过期")

        return attrs


class PhoneLoginSerializer(serializers.Serializer):
    """手机号验证码登录参数校验。"""

    phone = serializers.CharField()
    sms_code = serializers.CharField()

    def validate_phone(self, value):
        return validate_phone_format(value)

    def validate(self, attrs):
        phone = attrs["phone"]

        if not validate_sms_code(phone, "login", attrs["sms_code"]):
            raise serializers.ValidationError("短信验证码错误或已过期")

        return attrs


class SmsCodeSerializer(serializers.Serializer):
    """
    获取短信验证码参数校验。

    不同 purpose 有不同的手机号存在性要求：
    注册要求手机号未注册，登录/找回密码要求手机号已注册。
    """

    phone = serializers.CharField()
    purpose = serializers.ChoiceField(choices=sorted(SMS_PURPOSES))
    captcha_key = serializers.CharField()
    captcha_code = serializers.CharField()

    def validate_phone(self, value):
        return validate_phone_format(value)

    def validate(self, attrs):
        phone = attrs["phone"]
        purpose = attrs["purpose"]

        if not validate_captcha(attrs["captcha_key"], attrs["captcha_code"], consume=False):
            raise serializers.ValidationError("图形验证码错误或已过期")

        # 这里不改数据库结构，只按当前 User.phone 字段判断账号是否存在。
        user_exists = User.objects.filter(phone=phone).exists()

        if purpose == "register" and user_exists:
            raise serializers.ValidationError("手机号已注册")

        if purpose in {"reset_password", "login"} and not user_exists:
            raise serializers.ValidationError("手机号未注册")

        return attrs


class RegisterSerializer(serializers.Serializer):
    """
    注册参数校验。

    包含结构图里的手机号、真实姓名、身份证、密码、图形验证码、
    短信验证码和用户协议校验。
    """

    phone = serializers.CharField()
    real_name = serializers.CharField(max_length=50)
    id_card = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    captcha_key = serializers.CharField()
    captcha_code = serializers.CharField()
    sms_code = serializers.CharField()
    agreed = serializers.BooleanField()

    def validate_phone(self, value):
        phone = validate_phone_format(value)

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("手机号已注册")

        return phone

    def validate_real_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("真实姓名不能为空")

        if len(value) > 50:
            raise serializers.ValidationError("真实姓名长度不能超过50位")

        return value

    def validate_id_card(self, value):
        # validate_id_card 内部会做格式、出生日期、校验位算法验证。
        id_card = validate_id_card(value)

        if User.objects.filter(id_card=id_card).exists():
            raise serializers.ValidationError("身份证号已注册")

        return id_card

    def validate_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        # 跨字段校验放在 validate：两次密码、协议、验证码都需要多个字段一起判断。
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("两次密码不一致")

        if not attrs["agreed"]:
            raise serializers.ValidationError("请先阅读并勾选用户协议")

        if not validate_captcha(attrs["captcha_key"], attrs["captcha_code"]):
            raise serializers.ValidationError("图形验证码错误或已过期")

        if not validate_sms_code(attrs["phone"], "register", attrs["sms_code"]):
            raise serializers.ValidationError("短信验证码错误或已过期")

        return attrs

    def save(self):
        # 注册后先禁用账号，等待管理员审核通过后再启用。
        return User.objects.create_user(
            username=self.validated_data["phone"],
            phone=self.validated_data["phone"],
            real_name=self.validated_data["real_name"],
            id_card=self.validated_data["id_card"],
            password=self.validated_data["password"],
            status=0,
            is_active=False,
        )


class PasswordResetSerializer(serializers.Serializer):
    """找回密码参数校验。"""

    phone = serializers.CharField()
    sms_code = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_phone(self, value):
        phone = validate_phone_format(value)

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("手机号未注册")

        return phone

    def validate_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("两次密码不一致")

        if not validate_sms_code(attrs["phone"], "reset_password", attrs["sms_code"]):
            raise serializers.ValidationError("短信验证码错误或已过期")

        return attrs

    def save(self):
        # set_password 会使用 Django 的密码哈希算法，不能直接明文赋值。
        user = User.objects.get(phone=self.validated_data["phone"])
        user.set_password(self.validated_data["password"])
        user.save(update_fields=["password"])
        return user


class LogoutSerializer(serializers.Serializer):
    """退出登录参数；refresh 必须传入，后端会把它加入黑名单。"""

    refresh = serializers.CharField(required=True, allow_blank=False)
