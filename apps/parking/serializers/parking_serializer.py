from rest_framework import serializers

from apps.parking.models import Parking


class ParkingSerializer(serializers.ModelSerializer):

    owner_name = serializers.CharField(
        source="owner.name",
        read_only=True,
    )

    room_no = serializers.CharField(
        source="owner.house.room_no",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Parking
        fields = "__all__"
