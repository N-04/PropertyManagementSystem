from django.db import models


class Repair(models.Model):
    """
    报修管理
    """

    # 业主
    owner = models.ForeignKey(
        "owners.Owner",
        on_delete=models.CASCADE,
        related_name="repairs",
        verbose_name="报修业主",
    )
    # 房屋
    house = models.ForeignKey(
        "community.House",
        on_delete=models.CASCADE,
        related_name="repairs",
        verbose_name="房屋",
    )

    # 报修标题
    title = models.CharField(
        max_length=100,
        verbose_name="报修标题",
    )

    # 报修内容
    content = models.TextField(
        verbose_name="报修内容",
    )

    # 处理状态
    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "待派单"),
            ("assigned", "已派单"),
            ("processing", "处理中"),
            ("finished", "已完成"),
            ("closed", "已关闭"),
        ),
        default="pending",
        verbose_name="状态",
    )

    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "repair"
        verbose_name = "报修"
        verbose_name_plural = "报修管理"
