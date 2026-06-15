# 文件说明：配置 Django Admin 后台管理展示。

from django.contrib import admin
from apps.notice.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "created_at",
    )
