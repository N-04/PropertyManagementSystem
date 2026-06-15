# 文件说明：负责 apps/community/serializers/building_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.community.models import Building


class BuildingSerializer(serializers.ModelSerializer):
    """
    楼栋序列化器
    """

    community_name = serializers.CharField(
        source="community.name",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:

        model = Building

        fields = [
            "id",
            "community",
            "community_name",
            "name",
            "code",
            "floor_count",
            "unit_count",
            "created_at",
        ]
