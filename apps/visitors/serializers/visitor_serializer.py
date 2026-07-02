# 文件说明：负责 apps/visitors/serializers/visitor_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.visitors.models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    """

    访客序列化器

    """

    # 被访业主名称
    owner_name = serializers.CharField(source="owner.name", read_only=True)

    # 访客临停页面需要展示被访房屋，和业主车位列表区分开。
    room_no = serializers.SerializerMethodField()

    # 来访时间
    visit_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%Y-%m-%d %H:%M:%S"],
    )

    # 离开时间
    leave_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%Y-%m-%d %H:%M:%S"],
        allow_null=True,
        required=False,
    )

    # 审批时间
    approve_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%Y-%m-%d %H:%M:%S"],
        allow_null=True,
        required=False,
    )

    # 到访时间
    enter_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%Y-%m-%d %H:%M:%S"],
        allow_null=True,
        required=False,
    )

    # 审批人
    approve_user_name = serializers.CharField(
        source="approve_user.username", read_only=True
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Visitor

        fields = "__all__"

    def get_room_no(self, obj):
        return obj.owner.house.room_no if obj.owner_id and obj.owner.house_id else ""
