# 文件说明：配置 Django Admin 后台管理展示。

from django.contrib import admin

from apps.finance.models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "house",
        "fee_type",
        "amount",
        "deadline",
        "status",
        "created_at",
    )
