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
        # 车位号前缀承担业务含义：SM 为售卖车位，PT/P 为普通访客临停车位。
        parking_no = obj.parking_no or ""
        normalized_no = parking_no.strip().upper()

        if normalized_no.startswith("SM"):
            return "SM"

        if normalized_no.startswith("PT") or normalized_no.startswith("P"):
            return "PT"

        if "-" in normalized_no:
            return normalized_no.split("-", 1)[0]

        return (normalized_no[:1] or "其他")
