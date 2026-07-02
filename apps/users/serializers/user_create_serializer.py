# 文件说明：负责 apps/users/serializers/user_create_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.users.models import Role
from apps.users.models.user import User
from apps.users.serializers.role_serializer import RoleSerializer


class UserCreateSerializer(serializers.ModelSerializer):

    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "real_name",
            "phone",
            "password",
            "roles",
            "role_ids",
            "status",
            "created_at",
        ]

    def create(self, validated_data):

        role_ids = validated_data.pop("role_ids", [])

        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        roles = Role.objects.filter(id__in=role_ids)
        user.roles.set(roles)

        return user
