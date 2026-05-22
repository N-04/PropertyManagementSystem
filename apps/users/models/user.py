from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.users.models.role import Role

class User(AbstractUser):

    STATUS_CHOICES = (
        (1, '正常'),
        (0, '禁用'),
    )

    phone = models.CharField('手机号', max_length=11, unique=True)

    real_name = models.CharField('真实姓名', max_length=32)

    nickname = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='昵称'
    )

    id_card = models.CharField(
        '身份证',
        max_length=18,
        unique=True,
        null=True,
        blank=True
    )

    avatar = models.CharField(
        '头像',
        max_length=255,
        null=True,
        blank=True
    )

    status = models.SmallIntegerField(
        '状态',
        choices=STATUS_CHOICES,
        default=1
    )

    roles = models.ManyToManyField(
        'Role',
        verbose_name = '角色',
        blank = True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username