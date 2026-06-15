# 文件说明：配置 Django Admin 后台管理展示。

from django.contrib import admin

from apps.owners.models import Owner


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone",
        "id_card",
        "house",
        "created_at",
    )
