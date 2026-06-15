# 文件说明：配置 Django Admin 后台管理展示。

from django.contrib import admin

from apps.repairs.models import Repair


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):

    list_display = ("id", "house", "title", "status", "created_at")
