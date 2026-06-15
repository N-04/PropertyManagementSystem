# 文件说明：定义 apps/finance/models/fee.py 对应业务的数据模型和数据库映射。

from django.db import models
from apps.owners.models import Owner
from apps.community.models import House


class Fee(models.Model):
    """
    收费管理
    """

    STATUS_CHOICES = (
        ("unpaid", "未缴费"),
        ("paid", "已缴费"),
        ("overdue", "已逾期"),
    )
    TYPE_CHOICES = (
        ("property", "物业费"),
        ("water", "水费"),
        ("electric", "电费"),
        ("parking", "停车费"),
        ("other", "其他费用"),
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name="业主",
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="房屋",
    )
    fee_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name="费用类型",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="金额",
    )
    deadline = models.DateTimeField(
        verbose_name="缴费截止日期",
    )
    pay_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="缴费时间",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unpaid",
    )
    remark = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "fee"
