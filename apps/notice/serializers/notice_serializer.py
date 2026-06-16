# 文件说明：负责 apps/notice/serializers/notice_serializer.py 对应接口的数据序列化、反序列化和参数校验。

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
    notice_type_display = serializers.CharField(
        source="get_notice_type_display",
        read_only=True,
    )
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Notice
        fields = "__all__"
