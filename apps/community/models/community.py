from django.db import models


class Community(models.Model):

    name = models.CharField(
        '小区名称',
        max_length=64
    )

    code = models.CharField(
        '小区编码',
        max_length=32,
        unique=True
    )

    address = models.CharField(
        '地址',
        max_length=255
    )

    contact_person = models.CharField(
        '联系人',
        max_length=32,
        null=True,
        blank=True
    )

    contact_phone = models.CharField(
        '联系电话',
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
        db_table = 'community'
        verbose_name = '小区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name