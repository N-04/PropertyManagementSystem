from rest_framework import serializers

from apps.repairs.models import Repair


class RepairSerializer(serializers.ModelSerializer):
    """
    报修序列化器
    """

    owner_name = serializers.CharField(
        source="owner.name",
        read_only=True,
    )

    room_no = serializers.CharField(
        source="house.room_no",
        read_only=True,
    )

    unit_name = serializers.CharField(
        source="house.unit.name",
        read_only=True,
    )

    building_name = serializers.CharField(
        source="house.unit.building.name",
        read_only=True,
    )

    community_name = serializers.CharField(
        source="house.unit.building.community.name",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Repair

        fields = "__all__"
