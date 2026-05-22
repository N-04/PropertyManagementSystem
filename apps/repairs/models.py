from django.db import models

from apps.users.models import User

class Repair(models.Model):

    LEVEL_CHOICES = (
        ('normal', '普通'),
        ('urgent', '紧急')
    )

    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('finished', '已完成')
    )

    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='normal'
    )

    # status = models.CharField(
    #     max_length=20,
    #     choices=STATUS_CHOICES,
    #     default='pending'
    # )
    status = models.IntegerField(
    default=1,
    choices=(
        (1, '待处理'),
        (2, '处理中'),
        (3, '已完成'),
    )
)

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add = True
    )

class Meta:

        verbose_name = '报修'

        verbose_name_plural = '报修'