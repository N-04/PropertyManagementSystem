# 文件说明：配置 Django Admin 后台管理展示。

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models.menu import Menu
from apps.users.models.permission import Permission
from apps.users.models.role import Role
from apps.users.models.user import User


# 用户管理
@admin.register(User)
class UserAdmin(BaseUserAdmin):

    # 列表显示
    list_display = (
        "username",
        "id",
        "real_name",
        "phone",
        "is_active",
    )

    # 可搜索
    search_fields = ("username", "real_name")

    # 过滤
    list_filter = ("is_active",)

    # 编辑页
    filter_horizontal = ("roles",)

    fieldsets = (
        (
            "基础信息",
            {
                "fields": (
                    "username",
                    "password",
                    "real_name",
                    "phone",
                    "id_card",
                    "avatar",
                )
            },
        ),
        (
            "权限信息",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "roles",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "时间信息",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "real_name",
                    "phone",
                    "id_card",
                    "is_staff",
                    "is_superuser",
                    "roles",
                ),
            },
        ),
    )


# 角色管理
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "code")

    filter_horizontal = ("permissions",)


# 权限管理
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):

    list_display = ("name", "id", "code")


# 菜单管理
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ("id", "title", "path")
