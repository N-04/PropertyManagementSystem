# 文件说明：负责 apps/community/serializers/house_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.community.models import House


class HouseSerializer(serializers.ModelSerializer):
    """
    房屋序列化器
    """

    unit_name = serializers.CharField(
        source="unit.name",
        read_only=True,
    )

    building_name = serializers.CharField(
        source="unit.building.name",
        read_only=True,
    )

    community_name = serializers.CharField(
        source="unit.building.community.name",
        read_only=True,
    )

    community = serializers.IntegerField(
        source="unit.building.community_id",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = House

        fields = "__all__"
