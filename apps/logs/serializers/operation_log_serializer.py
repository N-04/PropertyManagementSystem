# 文件说明：负责 apps/logs/serializers/operation_log_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.logs.models.operation_log import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = OperationLog
        fields = "__all__"
