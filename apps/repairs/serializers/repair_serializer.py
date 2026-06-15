# 文件说明：负责 apps/repairs/serializers/repair_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.repairs.models import Repair


class RepairSerializer(serializers.ModelSerializer):
    """
    报修序列化器
    """

    repair_image_list = serializers.SerializerMethodField()
    result_image_list = serializers.SerializerMethodField()
    owner_name = serializers.CharField(
        source="owner.name",
        read_only=True,
    )

    status = serializers.CharField()
    status_text = serializers.CharField(source="get_status_display", read_only=True)

    phone = serializers.CharField(source="owner.phone", read_only=True)

    repair_user_name = serializers.SerializerMethodField()

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

    finish_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    evaluation_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        required=False,
        allow_null=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Repair
        fields = "__all__"

    def _split_images(self, value):
        if not value:
            return []

        return [item for item in value.split("|") if item]

    def get_repair_image_list(self, obj):
        return self._split_images(obj.repair_images)

    def get_result_image_list(self, obj):
        return self._split_images(obj.result_images)

    def get_repair_user_name(self, obj):

        return [user.username for user in obj.repair_user.all()]
