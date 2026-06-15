# 文件说明：负责 apps/logs/serializers/login_log_serializer.py 对应接口的数据序列化、反序列化和参数校验。

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
