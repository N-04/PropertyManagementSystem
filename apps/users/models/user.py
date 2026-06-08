from django.contrib.auth.models import AbstractUser
from django.db import models

from .role import Role


class User(AbstractUser):

    STATUS_CHOICES = (
        (1, "正常"),
        (0, "禁用"),
    )

    phone = models.CharField(
        max_length=11, verbose_name="手机号", blank=True, null=True
    )

    real_name = models.CharField(
        max_length=50, verbose_name="真实姓名", blank=True, null=True
    )

    nickname = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="昵称"
    )

    id_card = models.CharField(
        "身份证", max_length=18, unique=True, null=True, blank=True
    )

    avatar = models.CharField("头像", max_length=255, null=True, blank=True)

    status = models.SmallIntegerField("状态", choices=STATUS_CHOICES, default=1)

    roles = models.ManyToManyField(
        "Role", verbose_name="角色", blank=True, related_name="multi_role_users"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    role = models.ForeignKey(
        Role, null=True, on_delete=models.SET_NULL, related_name="role_users"
    )

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
