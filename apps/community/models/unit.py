from django.db import models


class Unit(models.Model):

    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name='所属楼栋'
    )

    name = models.CharField(
        '单元名称',
        max_length=32
    )

    code = models.CharField(
        '单元编码',
        max_length=32
    )

    floor_count = models.IntegerField(
        '楼层数',
        default=1
    )

    house_count = models.IntegerField(
        '房屋数量',
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
        db_table = 'unit'
        verbose_name = '单元'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name