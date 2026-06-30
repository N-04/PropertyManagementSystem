# 文件说明：定义 apps/parking/models/parking.py 对应业务的数据模型和数据库映射。

from django.db import models


class Parking(models.Model):
    """车位主表，记录车位归属、面积和使用状态。"""

    # owner 为空表示可绑定/可售卖或访客临停车位，绑定后才归属具体业主。
    owner = models.ForeignKey(
        "owners.Owner",
        on_delete=models.SET_NULL,
        related_name="parkings",
        null=True,
        blank=True,
        verbose_name="所属业主",
    )

    parking_no = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="车位号",
    )

    # 车位面积用于展示和计费，不直接决定普通/售卖分类。
    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="面积",
    )

    # idle 表示当前可分配，used 表示已被占用或绑定。
    status = models.CharField(
        max_length=20,
        choices=(
            ("idle", "空闲"),
            ("used", "使用中"),
        ),
        default="used",
        verbose_name="状态",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "parking"
