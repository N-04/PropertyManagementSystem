from rest_framework import serializers

from apps.notice.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    """
    公告序列化器
    """

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Notice
        fields = "__all__"
