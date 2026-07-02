# 文件说明：配置 Django Admin 后台管理展示。

from django.contrib import admin

from apps.parking.models.parking import Parking


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "parking_no",
        "area",
        "status",
    )
