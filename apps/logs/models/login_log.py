# 文件说明：定义 apps/logs/models/login_log.py 对应业务的数据模型和数据库映射。

from django.db import models


class LoginLog(models.Model):
    """
    登录日志
    """

    username = models.CharField(
        max_length=50,
        verbose_name="用户名",
    )

    ip = models.CharField(
        max_length=100,
        verbose_name="IP地址",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="登录时间",
    )

    class Meta:
        db_table = "login_log"
