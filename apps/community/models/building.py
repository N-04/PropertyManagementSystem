from django.db import models


class Building(models.Model):
    """
    楼栋
    """

    community = models.ForeignKey(
        "Community",
        on_delete=models.CASCADE,
        related_name="buildings",
        verbose_name="所属小区",
    )

    name = models.CharField(max_length=50, verbose_name="楼栋名称")

    code = models.CharField(max_length=50, unique=True, verbose_name="楼栋编码")

    floor_count = models.IntegerField(default=0, verbose_name="总楼层")

    unit_count = models.IntegerField(default=0, verbose_name="单元数")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "building"

    def __str__(self):
        return self.name
