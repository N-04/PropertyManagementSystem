from django.db import models


class OperationLog(models.Model):
    """
    操作日志
    """

    username = models.CharField(
        max_length=50,
        verbose_name="用户名",
    )

    module = models.CharField(
        max_length=50,
        verbose_name="模块",
    )

    action = models.CharField(
        max_length=200,
        verbose_name="操作内容",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "operation_log"
