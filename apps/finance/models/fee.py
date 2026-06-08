from django.db import models


class Fee(models.Model):
    """
    物业费
    """

    house = models.ForeignKey(
        "community.House",
        on_delete=models.CASCADE,
        related_name="fees",
        verbose_name="房屋",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="金额",
    )

    fee_type = models.CharField(
        max_length=30,
        choices=(
            ("property", "物业费"),
            ("parking", "车位费"),
            ("water", "水费"),
            ("electric", "电费"),
        ),
        default="property",
        verbose_name="费用类型",
    )

    fee_month = models.CharField(
        max_length=20,
        verbose_name="账单月份",
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ("unpaid", "未缴费"),
            ("paid", "已缴费"),
        ),
        default="unpaid",
    )

    pay_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    remark = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "fee"
