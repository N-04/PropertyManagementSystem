from django.db import models

from apps.owners.models import Owner
from apps.parking.models import Parking


class Car(models.Model):
    """
    车辆信息
    """

    # 关联业主
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name="所属业主",
    )

    # 车牌号
    plate_no = models.CharField(
        max_length=20,
        verbose_name="车牌号",
    )

    # 品牌
    brand = models.CharField(
        max_length=50,
        verbose_name="车辆品牌",
    )

    # 颜色
    color = models.CharField(
        max_length=20,
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

    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "car"
        verbose_name = "车辆"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plate_no
