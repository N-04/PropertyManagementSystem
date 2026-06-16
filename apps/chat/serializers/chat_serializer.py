# 文件说明：负责站内会话和消息接口的数据序列化。
from rest_framework import serializers

from apps.chat.models import ChatConversation, ChatMessage
from apps.users.utils.role_access import get_user_role_codes


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)
    sender_real_name = serializers.CharField(source="sender.real_name", read_only=True)
    sender_role_codes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "conversation",
            "sender",
            "sender_name",
            "sender_real_name",
            "sender_role_codes",
            "content",
            "message_type",
            "created_at",
        ]
        read_only_fields = ["conversation", "sender", "message_type"]

    def get_sender_role_codes(self, obj):
        return sorted(get_user_role_codes(obj.sender))


class ChatConversationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)
    created_by_real_name = serializers.CharField(source="created_by.real_name", read_only=True)
    target_role_text = serializers.CharField(source="get_target_role_display", read_only=True)
    status_text = serializers.CharField(source="get_status_display", read_only=True)
    end_reason_text = serializers.CharField(source="get_end_reason_display", read_only=True)
    participant_names = serializers.SerializerMethodField()
    messages = ChatMessageSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ended_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    rating_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ChatConversation
        fields = [
            "id",
            "title",
            "target_role",
            "target_role_text",
            "status",
            "status_text",
            "end_reason",
            "end_reason_text",
            "created_by",
            "created_by_name",
            "created_by_real_name",
            "participant_names",
            "last_message",
            "messages",
            "ended_at",
            "rating_score",
            "rating_comment",
            "rating_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_by",
            "last_message",
            "end_reason",
            "ended_at",
            "rating_score",
            "rating_comment",
            "rating_at",
        ]

    def get_participant_names(self, obj):
        return [
            item.real_name or item.username
            for item in obj.participants.all().order_by("id")
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("会话标题不能为空")

        if len(value) > 120:
            raise serializers.ValidationError("会话标题不能超过120个字符")

        return value
