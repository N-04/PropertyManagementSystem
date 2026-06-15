# 文件说明：配置 Django 应用元信息。

from django.apps import AppConfig


class OwnersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.owners'
