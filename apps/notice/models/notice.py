from django.db import models


class Notice(models.Model):
    """
    公告
    """

    title = models.CharField(
        max_length=200,
        verbose_name="公告标题",
    )

    content = models.TextField(
        verbose_name="公告内容",
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
