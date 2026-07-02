# 文件说明：负责 apps/users/serializers/user_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from apps.community.models import House
from apps.owners.models import Owner
from apps.users.models.user import User
from apps.users.serializers.role_serializer import RoleSerializer
from apps.users.utils.role_access import is_owner_user
from apps.users.utils.validators import (
    mask_id_card,
    validate_password_strength,
    validate_phone_format,
)


class UserSerializer(serializers.ModelSerializer):
    """用户列表/详情序列化器，返回角色和脱敏身份证。"""

    roles = RoleSerializer(many=True, read_only=True)
    id_card_masked = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "real_name",
            "phone",
            "id_card_masked",
            "roles",
            "status",
            "is_active",
            "created_at",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        roles = validated_data.pop("roles", [])

        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        user.roles.set(roles)

        return user

    def get_id_card_masked(self, obj):
        # 对外展示身份证时只返回脱敏后的字符串。
        return mask_id_card(obj.id_card)


class UserInfoSerializer(serializers.ModelSerializer):
    """当前登录用户信息序列化器。"""

    id_card_masked = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    role_codes = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "real_name",
            "phone",
            "nickname",
            "avatar",
            "status",
            "id_card_masked",
            "roles",
            "role_codes",
        ]

    def get_id_card_masked(self, obj):
        if obj.id_card:
            return mask_id_card(obj.id_card)

        if is_owner_user(obj) and obj.phone:
            owner = Owner.objects.filter(phone=obj.phone).first()

            if owner:
                return mask_id_card(owner.id_card)

        return ""

    def get_roles(self, obj):
        roles = list(obj.roles.values_list("name", flat=True))

        if obj.role_id and obj.role.name not in roles:
            roles.append(obj.role.name)

        return roles

    def get_role_codes(self, obj):
        role_codes = list(obj.roles.values_list("code", flat=True))

        if obj.role_id and obj.role.code not in role_codes:
            role_codes.append(obj.role.code)

        if obj.is_superuser and "super_admin" not in role_codes:
            role_codes.append("super_admin")

        return role_codes


class CurrentUserProfileSerializer(serializers.Serializer):
    """当前用户资料修改校验。"""

    username = serializers.CharField(required=False, max_length=150)
    real_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=50)
    phone = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.CharField(required=False, allow_blank=True, max_length=255)
    house_id = serializers.IntegerField(required=False, allow_null=True)
    relationship = serializers.ChoiceField(
        required=False,
        choices=["self", "spouse", "child", "parent", "other"],
    )

    def validate_username(self, value):
        username = value.strip()

        if not username:
            raise serializers.ValidationError("用户名不能为空")

        UnicodeUsernameValidator()(username)

        user = self.context["request"].user

        if User.objects.exclude(id=user.id).filter(username=username).exists():
            raise serializers.ValidationError("用户名已被其他账号使用")

        return username

    def validate_phone(self, value):
        if not value:
            return value

        phone = validate_phone_format(value)
        user = self.context["request"].user

        if User.objects.exclude(id=user.id).filter(phone=phone).exists():
            raise serializers.ValidationError("手机号已被其他账号使用")

        if is_owner_user(user):
            owner_queryset = Owner.objects.filter(phone=user.phone)
            owner_ids = list(owner_queryset.values_list("id", flat=True))

            if Owner.objects.exclude(id__in=owner_ids).filter(phone=phone).exists():
                raise serializers.ValidationError("手机号已被其他业主使用")

        return phone

    def validate_house_id(self, value):
        if value is None:
            return value

        house = House.objects.filter(id=value).first()

        if not house:
            raise serializers.ValidationError("选择的房屋不存在")

        user = self.context["request"].user

        if is_owner_user(user):
            owner_queryset = Owner.objects.filter(house=house)
            is_current_user_house = owner_queryset.filter(phone=user.phone).exists()

            if is_current_user_house:
                return value

            if house.status != "vacant" or owner_queryset.exists():
                raise serializers.ValidationError("只能选择未绑定的闲置房屋")

        return value

    def validate(self, attrs):
        user = self.context["request"].user
        house_id = attrs.get("house_id")

        if house_id and is_owner_user(user):
            real_name = attrs.get("real_name") or user.real_name
            phone = attrs.get("phone") or user.phone

            if not real_name:
                raise serializers.ValidationError("绑定房屋前请先填写真实姓名")

            if not phone:
                raise serializers.ValidationError("绑定房屋前请先填写手机号")

            if not user.id_card:
                raise serializers.ValidationError("绑定房屋前请先完善身份证信息")

            owner_queryset = Owner.objects.filter(phone=user.phone)

            if not owner_queryset.exists():
                same_id_card_owner = Owner.objects.filter(id_card=user.id_card).first()

                if same_id_card_owner and same_id_card_owner.house_id != house_id:
                    raise serializers.ValidationError("该身份证已绑定其他房屋")

        return attrs

    def update(self, instance, validated_data):
        house_id = validated_data.pop("house_id", None)
        relationship = validated_data.pop("relationship", None)
        old_phone = instance.phone
        owner_updates = {}

        for field in ["username", "real_name", "nickname", "phone", "avatar"]:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        if "real_name" in validated_data:
            owner_updates["name"] = validated_data["real_name"]

        if "phone" in validated_data and validated_data["phone"]:
            owner_updates["phone"] = validated_data["phone"]

        if "avatar" in validated_data:
            owner_updates["avatar"] = validated_data["avatar"]

        if house_id and is_owner_user(instance):
            owner_updates["house_id"] = house_id

        if relationship and is_owner_user(instance):
            owner_updates["relationship"] = relationship

        if validated_data:
            instance.save(update_fields=list(validated_data.keys()))

        if owner_updates and is_owner_user(instance):
            owner_queryset = Owner.objects.filter(phone=old_phone)

            if owner_queryset.exists():
                owner_queryset.update(**owner_updates)
            elif house_id:
                matched_owner = Owner.objects.filter(
                    house_id=house_id,
                    id_card=instance.id_card,
                ).first()

                if matched_owner:
                    for field, value in owner_updates.items():
                        setattr(matched_owner, field, value)

                    matched_owner.status = "approved"
                    matched_owner.save()
                else:
                    Owner.objects.create(
                        house_id=house_id,
                        name=instance.real_name or instance.username,
                        phone=instance.phone,
                        avatar=instance.avatar,
                        relationship=relationship or "self",
                        id_card=instance.id_card,
                        is_primary=True,
                        status="approved",
                    )

            if house_id:
                owner_count = Owner.objects.filter(house_id=house_id).count()
                House.objects.filter(id=house_id).update(
                    status="occupied",
                    owner_count=owner_count,
                    resident_count=owner_count,
                )

        return instance


class CurrentUserPasswordSerializer(serializers.Serializer):
    """当前用户修改密码校验。"""

    old_password = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("原密码不正确")

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("两次密码不一致")

        return attrs


class UserAuditSerializer(serializers.Serializer):
    """
    用户审核序列化器。

    不新增审核状态字段，审核通过时启用账号，驳回时禁用账号。
    """

    audit_status = serializers.ChoiceField(choices=["approved", "rejected"])

    def update(self, instance, validated_data):
        if validated_data["audit_status"] == "approved":
            instance.is_active = True
            instance.status = 1
        else:
            instance.is_active = False
            instance.status = 0

        instance.save(update_fields=["is_active", "status"])

        return instance
