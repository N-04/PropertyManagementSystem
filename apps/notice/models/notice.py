# 文件说明：定义 apps/notice/models/notice.py 对应业务的数据模型和数据库映射。

from django.db import models


class Notice(models.Model):
    """
    公告
    """

    TYPE_CHOICES = (
        ("general", "系统公告"),
        ("activity", "活动通知"),
        ("finance", "财务公告"),
        ("repair", "维修公告"),
    )

    title = models.CharField(
        max_length=200,
        verbose_name="公告标题",
    )

    content = models.TextField(
        verbose_name="公告内容",
    )

    notice_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="general",
        verbose_name="公告类型",
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ("draft", "草稿"),
            ("published", "已发布"),
        ),
        default="published",
        verbose_name="状态",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "notice"

    def __str__(self):
        return self.title
