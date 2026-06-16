# 文件说明：负责 apps/parking/serializers/parking_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.parking.models import Parking


class ParkingSerializer(serializers.ModelSerializer):

    owner_name = serializers.SerializerMethodField()

    room_no = serializers.SerializerMethodField()

    status_text = serializers.CharField(source="get_status_display", read_only=True)

    zone = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Parking
        fields = "__all__"

    def get_owner_name(self, obj):
        return obj.owner.name if obj.owner_id else ""

    def get_room_no(self, obj):
        return obj.owner.house.room_no if obj.owner_id and obj.owner.house_id else ""

    def get_zone(self, obj):
        # 车位号通常以 A-001、B001 等格式录入，前缀用于前端分区展示。
        parking_no = obj.parking_no or ""
        if "-" in parking_no:
            return parking_no.split("-", 1)[0].upper()

        return (parking_no[:1] or "其他").upper()
