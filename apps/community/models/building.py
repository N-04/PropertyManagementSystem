from django.db import models


class Building(models.Model):

    community = models.ForeignKey(
        'Community',
        on_delete=models.CASCADE,
        verbose_name='所属小区'
    )

    name = models.CharField(
        '楼栋名称',
        max_length=32
    )

    code = models.CharField(
        '楼栋编码',
        max_length=32
    )

    floor_count = models.IntegerField(
        '楼层数',
        default=1
    )

    unit_count = models.IntegerField(
        '单元数',
        default=1
    )

    status = models.SmallIntegerField(
        '状态',
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'building'
        verbose_name = '楼栋'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name