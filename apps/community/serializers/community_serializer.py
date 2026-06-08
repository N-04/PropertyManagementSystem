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
