# 文件说明：定义 apps/community/models/unit.py 对应业务的数据模型和数据库映射。

from django.db import models


class Unit(models.Model):
    """
    单元
    """

    building = models.ForeignKey(
        "Building",
        on_delete=models.CASCADE,
        related_name="units",
        verbose_name="所属楼栋",
    )

    name = models.CharField(max_length=50, verbose_name="单元名称")

    code = models.CharField(max_length=50, unique=True, verbose_name="单元编码")

    floor_count = models.IntegerField(default=0, verbose_name="楼层数")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "unit"

    def __str__(self):
        return self.name
