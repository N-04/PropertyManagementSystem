# 文件说明：负责 apps/users/serializers/role_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.users.models.role import Role
from apps.users.models.permission import Permission


class PermissionSimpleSerializer(serializers.ModelSerializer):
    """
    权限简易序列化器

    用于角色详情展示
    """

    class Meta:
        model = Permission

        fields = [
            "id",
            "name",
            "code",
        ]


class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化器
    """

    # 角色拥有的权限
    permissions = PermissionSimpleSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Role

        fields = [
            "id",
            "name",
            "code",
            "permissions",
            "created_at",
        ]

        read_only_fields = [
            "created_at",
        ]
