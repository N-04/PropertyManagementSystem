# 文件说明：定义 apps/users/models/permission.py 对应业务的数据模型和数据库映射。

from django.db import models

from .menu import Menu


class Permission(models.Model):
    """
    权限表
    """

    name = models.CharField(
        max_length=50,
        verbose_name="权限名称",
    )

    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="权限编码",
    )

    menu = models.ForeignKey(
        Menu,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="菜单",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "sys_permission"
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
