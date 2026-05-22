from django.db import models


class Parking(models.Model):

    owner = models.ForeignKey(
        'owners.Owner',
        on_delete=models.CASCADE,
        verbose_name='所属业主'
    )

    plate_number = models.CharField(
        '车牌号',
        max_length=16,
        unique=True
    )

    car_brand = models.CharField(
        '车辆品牌',
        max_length=32,
        null=True,
        blank=True
    )

    car_model = models.CharField(
        '车型',
        max_length=32,
        null=True,
        blank=True
    )

    parking_no = models.CharField(
        '车位号',
        max_length=32
    )

    status = models.SmallIntegerField(
        '状态',
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'parking'
        verbose_name = '车位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plate_number