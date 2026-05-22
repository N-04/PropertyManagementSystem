from rest_framework import serializers

from apps.users.models.user import User
from apps.users.models.role import Role


class UserSerializer(serializers.ModelSerializer):

    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User

        fields = '__all__'

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):

        roles = validated_data.pop('roles', [])

        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        user.roles.set(roles)

        return user


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'nickname',
            'avatar',
            'status'
        ]