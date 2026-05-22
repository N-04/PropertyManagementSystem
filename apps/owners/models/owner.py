from django.db import models


class Owner(models.Model):

    house = models.ForeignKey(
        'community.House',
        on_delete=models.CASCADE,
        verbose_name='所属房屋'
    )

    name = models.CharField(
        '业主姓名',
        max_length=32
    )

    phone = models.CharField(
        '手机号',
        max_length=11
    )

    id_card = models.CharField(
        '身份证号',
        max_length=18,
        unique=True
    )

    gender = models.SmallIntegerField(
        '性别',
        default=1
    )

    birthday = models.DateField(
        '出生日期',
        null=True,
        blank=True
    )

    address = models.CharField(
        '联系地址',
        max_length=255,
        null=True,
        blank=True
    )

    emergency_contact = models.CharField(
        '紧急联系人',
        max_length=32,
        null=True,
        blank=True
    )

    emergency_phone = models.CharField(
        '紧急联系电话',
        max_length=11,
        null=True,
        blank=True
    )

    status = models.SmallIntegerField(
        '状态',
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'owner'
        verbose_name = '业主'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name