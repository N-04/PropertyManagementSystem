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
