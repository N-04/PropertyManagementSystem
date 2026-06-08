from rest_framework import serializers

from apps.users.models.user import User
from apps.users.serializers.role_serializer import RoleSerializer
from apps.users.utils.validators import mask_id_card


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

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "nickname",
            "avatar",
            "status",
            "id_card_masked",
        ]

    def get_id_card_masked(self, obj):
        return mask_id_card(obj.id_card)


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
