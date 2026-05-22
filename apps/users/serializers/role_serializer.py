from rest_framework import serializers

from apps.users.models.role import Role
from apps.users.models.permission import Permission
from apps.users.models.menu import Menu


class RoleSerializer(serializers.ModelSerializer):

    permissions = serializers.PrimaryKeyRelatedField(
        queryset = Permission.objects.all(),
        many = True,
        required = False
    )

    menus = serializers.PrimaryKeyRelatedField(
        queryset = Menu.objects.all(),
        many = True,
        required = False
    )

    class Meta:
        model = Role

        fields = '__all__'