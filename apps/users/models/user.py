# 文件说明：定义 apps/users/models/user.py 对应业务的数据模型和数据库映射。

from django.contrib.auth.models import AbstractUser
from django.db import models

from .role import Role


class User(AbstractUser):
    """
    系统用户表。

    这里保持和已有 users 迁移一致，避免启动时因为模型字段和数据库结构不一致
    影响 superadmin 登录和后台管理。
    """

    STATUS_CHOICES = (
        (1, "正常"),
        (0, "禁用"),
    )

    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="手机号",
    )

    real_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="真实姓名",
    )

    nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="昵称",
    )

    id_card = models.CharField(
        max_length=18,
        unique=True,
        blank=True,
        null=True,
        verbose_name="身份证",
    )

    avatar = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="头像",
    )

    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=1,
        verbose_name="账号状态",
    )

    roles = models.ManyToManyField(
        "Role",
        verbose_name="角色",
        blank=True,
        related_name="multi_role_users",
    )

    role = models.ForeignKey(
        Role,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="role_users",
        verbose_name="主角色",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
