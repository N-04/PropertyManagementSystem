from django.contrib import admin
from apps.notice.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "created_at",
    )
