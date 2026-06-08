from rest_framework import serializers

from apps.cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    """
    车辆序列化器
    """

    owner_name = serializers.CharField(
        source="owner.name",
        read_only=True,
    )

    parking_no = serializers.CharField(
        source="parking.parking_no",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Car

        fields = [
            "id",
            "owner",
            "owner_name",
            "plate_no",
            "brand",
            "color",
            "parking",
            "parking_no",
            "created_at",
        ]
