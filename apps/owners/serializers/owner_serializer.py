# 文件说明：负责 apps/owners/serializers/owner_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.owners.models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    """业主资料序列化器，补充身份证脱敏和房屋层级展示字段。"""

    id_card_mask = serializers.SerializerMethodField()

    def get_id_card_mask(self, obj):
        """身份证仅展示前 6 后 4 位，避免前端暴露完整敏感信息。"""

        return obj.id_card[:6] + "********" + obj.id_card[-4:]

    # 头像只读，实际上传由文件上传接口返回 URL 后再写入业务资料。
    avatar = serializers.ImageField(read_only=True)

    # 兼容旧前端字段名，保持头像字段在历史表单中的读取方式不变。
    type = avatar

    # 房屋层级字段仅用于展示，写入绑定关系时仍使用 house 主键。
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
        # 业主资料字段随注册/认证流程变化较多，保持模型字段全量输出。
        fields = "__all__"
        extra_kwargs = {
            # 完整身份证号只允许写入，不再通过列表/详情接口明文返回。
            "id_card": {"write_only": True},
        }
