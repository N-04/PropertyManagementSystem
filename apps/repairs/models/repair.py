# 文件说明：定义 apps/repairs/models/repair.py 对应业务的数据模型和数据库映射。

from django.db import models

from apps.community.models import House
from apps.owners.models import Owner
from apps.users.models import User


class Repair(models.Model):
    """
    报修管理
    """

    STATUS_CHOICES = (
        ("pending", "待派单"),
        ("assigned", "待接单"),
        ("accepted", "已接单"),
        ("processing", "维修中"),
        ("finished", "已完成"),
    )
    # 业主
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name="报修业主",
    )

    # 房屋
    house = models.ForeignKey(
        House,
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

    # 报修图片，多个文件路径使用 | 分隔。
    repair_images = models.TextField(
        blank=True,
        default="",
        verbose_name="报修图片",
    )

    # 联系电话
    phone = models.CharField(max_length=20, blank=True, verbose_name="联系电话")

    # 维修人员
    repair_user = models.ManyToManyField(
        User,
        blank=True,
        verbose_name="维修人员",
    )

    # 处理状态
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # 完成时间
    finish_time = models.DateTimeField(
        verbose_name="完成时间",
        null=True,
        blank=True,
    )

    # 维修结果说明
    repair_result = models.TextField(
        blank=True,
        default="",
        verbose_name="维修结果",
    )

    # 维修结果图片，多个文件路径使用 | 分隔。
    result_images = models.TextField(
        blank=True,
        default="",
        verbose_name="维修结果图片",
    )

    # 业主维修评分，0.5-5.0 分，支持半星。
    evaluation_score = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="维修评分",
    )

    # 业主维修评价内容
    evaluation_content = models.TextField(
        blank=True,
        default="",
        verbose_name="维修评价",
    )

    # 评价时间
    evaluation_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="评价时间",
    )

    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "repair"
        verbose_name = "报修"
        verbose_name_plural = "报修管理"


# 维修日志
class RepairLog(models.Model):

    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)

    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    action = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
