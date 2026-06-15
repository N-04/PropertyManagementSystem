# 文件说明：注册投诉建议模型到 Django Admin。
from django.contrib import admin

from apps.complaints.models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "status", "phone", "created_at")
    list_filter = ("category", "status")
    search_fields = ("title", "content", "phone", "owner__name")
