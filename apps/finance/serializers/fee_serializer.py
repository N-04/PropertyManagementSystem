# 文件说明：负责 apps/finance/serializers/fee_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.finance.models import Fee


class FeeSerializer(serializers.ModelSerializer):
    """费用账单序列化器，统一输出账单基础信息和关联房屋展示字段。"""

    # 关联字段均为列表展示字段，写入时仍以 owner/house 主键为准。
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

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    deadline = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
    )

    pay_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    fee_type_text = serializers.CharField(
        source="get_fee_type_display",
        read_only=True,
    )

    status_text = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    payment_method_text = serializers.CharField(
        source="get_payment_method_display",
        read_only=True,
    )

    class Meta:
        model = Fee
        # 费用模块字段较稳定，直接透出模型字段并补充上方展示字段。
        fields = "__all__"
