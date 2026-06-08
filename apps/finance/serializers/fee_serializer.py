from rest_framework import serializers

from apps.finance.models import Fee


class FeeSerializer(serializers.ModelSerializer):

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

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Fee
        fields = "__all__"
