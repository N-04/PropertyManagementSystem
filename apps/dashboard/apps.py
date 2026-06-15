# 文件说明：配置 Django 应用元信息。

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    # 应用名称
    name = "apps.dashboard"

    verbose_name = "数据统计"
