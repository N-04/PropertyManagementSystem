# 文件说明：定义 apps/users/models/role.py 对应业务的数据模型和数据库映射。

from django.db import models


class Role(models.Model):
    """
    角色表
    """

    name = models.CharField(
        max_length=50,
        verbose_name="角色名称",
    )

    code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="角色编码",
    )

    permissions = models.ManyToManyField(
        "Permission",
        blank=True,
        related_name="roles",
        verbose_name="权限",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "users_role"
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
