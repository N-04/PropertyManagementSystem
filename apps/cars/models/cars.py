# 文件说明：定义 apps/cars/models/cars.py 对应业务的数据模型和数据库映射。

from django.db import models

from apps.owners.models import Owner
from apps.parking.models import Parking


class Car(models.Model):
    """
    车辆信息
    """

    # 车辆类型
    TYPE_CHOICES = (("monthly", "月租车"), ("temporary", "临时车"))

    STATUS_CHOICES = ("normal", "正常"), ("disabled", "禁用")

    # 关联业主
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="所属业主")

    # 品牌
    brand = models.CharField(max_length=30, blank=True, null=True, verbose_name="颜色")

    # 车牌号
    plate_no = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="车牌号",
    )

    # 颜色
    color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="车辆颜色",
    )

    # 绑定车位
    parking = models.ForeignKey(
        Parking,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="绑定车位",
    )

    car_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="monthly", verbose_name="车辆类型"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="normal",
        verbose_name="状态",
    )

    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "car"
        verbose_name = "车辆管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plate_no
