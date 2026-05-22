from django.db import models


class House(models.Model):

    unit = models.ForeignKey(
        'Unit',
        on_delete=models.CASCADE,
        verbose_name='所属单元'
    )

    house_no = models.CharField(
        '房号',
        max_length=32
    )

    floor = models.IntegerField(
        '楼层'
    )

    area = models.DecimalField(
        '建筑面积',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    inner_area = models.DecimalField(
        '套内面积',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    house_type = models.CharField(
        '户型',
        max_length=32,
        null=True,
        blank=True
    )

    usage = models.CharField(
        '用途',
        max_length=32,
        default='住宅'
    )

    status = models.SmallIntegerField(
        '状态',
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'house'
        verbose_name = '房屋'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.house_no