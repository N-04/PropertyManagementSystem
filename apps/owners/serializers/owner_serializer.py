# 文件说明：负责 apps/owners/serializers/owner_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.owners.models import Owner


class OwnerSerializer(serializers.ModelSerializer):

    id_card_mask = serializers.SerializerMethodField()

    def get_id_card_mask(self, obj):

        return obj.id_card[:6] + "********" + obj.id_card[-4:]

    avatar = serializers.ImageField(read_only=True)

    type = avatar

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
        model = Owner
        fields = "__all__"
