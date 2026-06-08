from django.db import models


class House(models.Model):
    """
    房屋
    """

    STATUS_CHOICES = (
        ("vacant", "空置"),
        ("occupied", "已入住"),
        ("renting", "出租"),
        ("repairing", "装修中"),
    )

    unit = models.ForeignKey(
        "Unit", on_delete=models.CASCADE, related_name="houses", verbose_name="所属单元"
    )

    room_no = models.CharField(max_length=20, verbose_name="房号")

    area = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="建筑面积"
    )

    house_type = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="户型"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="vacant", verbose_name="状态"
    )

    owner_count = models.IntegerField(default=0, verbose_name="业主数量")

    resident_count = models.IntegerField(default=0, verbose_name="居住人数")

    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "house"

    def __str__(self):
        return self.room_no
