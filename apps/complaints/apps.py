# 文件说明：配置投诉建议模块应用。
from django.apps import AppConfig


class ComplaintsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.complaints"
    verbose_name = "投诉建议"
