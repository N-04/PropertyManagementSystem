# 文件说明：负责投诉建议接口的数据序列化和参数校验。
from rest_framework import serializers

from apps.complaints.models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.name", read_only=True)
    category_text = serializers.CharField(source="get_category_display", read_only=True)
    status_text = serializers.CharField(source="get_status_display", read_only=True)
    handler_name = serializers.CharField(source="handler.username", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Complaint
        fields = "__all__"
        read_only_fields = ("handler",)

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("标题不能为空")

        if len(value) > 100:
            raise serializers.ValidationError("标题不能超过100个字符")

        return value

    def validate_content(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("内容不能为空")

        return value
