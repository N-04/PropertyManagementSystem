# 文件说明：负责投诉建议接口的数据序列化和参数校验。
from rest_framework import serializers

from apps.complaints.models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    """投诉建议读写序列化器，同时补充前端列表需要的展示字段。"""

    # 以下字段来自关联对象或 choice 展示值，只用于列表/详情展示，不参与写入。
    owner_name = serializers.CharField(source="owner.name", read_only=True)
    category_text = serializers.CharField(source="get_category_display", read_only=True)
    status_text = serializers.CharField(source="get_status_display", read_only=True)
    handler_name = serializers.CharField(source="handler.username", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Complaint
        fields = "__all__"
        # 处理人由后台处理接口自动记录，避免客户端伪造 handler。
        read_only_fields = ("handler",)

    def validate_title(self, value):
        """标题需要去掉前后空格后再做必填和长度校验。"""
        value = value.strip()

        if not value:
            raise serializers.ValidationError("标题不能为空")

        if len(value) > 100:
            raise serializers.ValidationError("标题不能超过100个字符")

        return value

    def validate_content(self, value):
        """投诉内容不能为空；空白字符不算有效内容。"""
        value = value.strip()

        if not value:
            raise serializers.ValidationError("内容不能为空")

        return value
