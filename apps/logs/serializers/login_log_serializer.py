from rest_framework import serializers
from apps.logs.models.login_log import LoginLog


class LoginLogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = LoginLog
        fields = "__all__"
