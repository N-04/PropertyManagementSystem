from django.contrib import admin

from apps.chat.models import ChatConversation, ChatMessage


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "target_role", "status", "created_by", "updated_at")
    list_filter = ("target_role", "status")
    search_fields = ("title", "last_message", "created_by__username", "created_by__real_name")
    filter_horizontal = ("participants",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "message_type", "created_at")
    list_filter = ("message_type",)
    search_fields = ("content", "sender__username", "sender__real_name")
