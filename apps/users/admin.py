from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models.role import Role
from apps.users.models.user import User
from apps.users.models.permission import Permission
from apps.users.models.menu import Menu

admin.site.register(Menu)
admin.site.register(Role)
admin.site.register(Permission)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'real_name',
        'phone',
        'status',
        'is_staff',
    )

    search_fields = (
        'username',
        'phone',
        'real_name',
    )