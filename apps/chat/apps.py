# 文件说明：配置 chat 应用元信息。
from django.apps import AppConfig


class ChatConfig(AppConfig):
    # 使用 BigAutoField 与项目其他业务表主键策略保持一致。
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.chat"
    verbose_name = "站内会话"
