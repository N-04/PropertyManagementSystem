from django.contrib import admin
from apps.finance.models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "house",
        "fee_month",
        "amount",
        "status",
    )
