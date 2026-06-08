from django.contrib import admin
from apps.community.models import Building, Community, Unit, House


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    """
    小区管理
    """

    list_display = (
        "id",
        "name",
        "code",
        "contact_name",
        "contact_phone",
        "created_at",
    )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "community",
        "name",
        "code",
        "floor_count",
        "unit_count",
        "created_at",
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):

    list_display = ("id", "building", "name", "code", "floor_count", "created_at")


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "unit",
        "room_no",
        "area",
        "status",
        "owner_count",
        "resident_count",
        "created_at",
    )
