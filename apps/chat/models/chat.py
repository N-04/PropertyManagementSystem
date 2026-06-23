# 文件说明：定义站内即时通讯会话和消息模型。
from django.conf import settings
from django.db import models


class ChatConversation(models.Model):
    STATUS_CHOICES = (
        ("active", "沟通中"),
        ("resolved", "已解决"),
        ("closed", "已关闭"),
    )
    END_REASON_CHOICES = (
        ("manual", "人工结束"),
        ("timeout", "超时结束"),
    )

    TARGET_ROLE_CHOICES = (
        ("owner", "业主"),
        ("customer_service", "客服人员"),
        ("finance_staff", "财务人员"),
        ("repair_staff", "维修员"),
        ("property_admin", "物业管理员"),
    )

    title = models.CharField(max_length=120, verbose_name="会话标题")
    target_role = models.CharField(
        max_length=40,
        choices=TARGET_ROLE_CHOICES,
        default="customer_service",
        verbose_name="目标角色",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="会话状态",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_chat_conversations",
        verbose_name="发起人",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chat_conversations",
        blank=True,
        verbose_name="参与人",
    )
    last_message = models.TextField(blank=True, default="", verbose_name="最后消息")
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    end_reason = models.CharField(
        max_length=20,
        choices=END_REASON_CHOICES,
        null=True,
        blank=True,
        verbose_name="结束原因",
    )
    rating_score = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="服务评分",
    )
    rating_comment = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="服务评价",
    )
    rating_at = models.DateTimeField(null=True, blank=True, verbose_name="评分时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "chat_conversation"
        ordering = ["-updated_at", "-id"]
        verbose_name = "站内会话"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ("text", "文本"),
        ("system", "系统"),
    )

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="所属会话",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name="发送人",
    )
    content = models.TextField(verbose_name="消息内容")
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPE_CHOICES,
        default="text",
        verbose_name="消息类型",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    class Meta:
        db_table = "chat_message"
        ordering = ["created_at", "id"]
        verbose_name = "站内消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:30]
