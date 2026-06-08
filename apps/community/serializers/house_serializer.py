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

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = House

        fields = "__all__"
