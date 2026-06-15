# 文件说明：负责 apps/community/serializers/community_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.community.models import Community


class CommunitySerializer(serializers.ModelSerializer):
    """
    小区序列化器
    """

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Community

        fields = "__all__"
