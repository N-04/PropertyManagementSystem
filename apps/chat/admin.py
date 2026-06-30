# 文件说明：注册站内会话和消息模型到 Django Admin，便于后台排查沟通记录。
from django.contrib import admin

from apps.chat.models import ChatConversation, ChatMessage


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    # 会话列表重点展示角色关系和最新更新时间，方便定位未处理沟通。
    list_display = ("id", "title", "target_role", "status", "created_by", "updated_at")
    list_filter = ("target_role", "status")
    search_fields = ("title", "last_message", "created_by__username", "created_by__real_name")
    filter_horizontal = ("participants",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # 消息列表保留发送人和消息类型，方便审计系统消息与用户消息。
    list_display = ("id", "conversation", "sender", "message_type", "created_at")
    list_filter = ("message_type",)
    search_fields = ("content", "sender__username", "sender__real_name")
