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
