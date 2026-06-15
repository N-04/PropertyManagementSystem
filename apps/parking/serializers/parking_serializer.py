# 文件说明：负责 apps/parking/serializers/parking_serializer.py 对应接口的数据序列化、反序列化和参数校验。

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
