from django.db import models
from apps.users.models.menu import Menu
from .permission import Permission


# =====================================================
# 角色表
# =====================================================
class Role(models.Model):

    # =====================================================
    # 角色名称
    # =====================================================
    name = models.CharField(max_length=50, verbose_name="角色名称")

    # =====================================================
    # 角色编码
    # =====================================================
    code = models.CharField(
        # 最大长度
        max_length=50,
        # 允许为空
        null=True,
        # 允许空字符串
        blank=True,
        # 备注
        verbose_name="角色编码",
    )

    permissions = models.ManyToManyField(
        Permission, blank=True, verbose_name="角色权限"
    )

    # =====================================================
    # 创建时间
    # =====================================================
    created_at = models.DateTimeField(
        # 自动创建
        auto_now_add=True,
        # 备注
        verbose_name="创建时间",
    )

    # =====================================================
    # 后台显示名称
    # =====================================================
    def __str__(self):

        return self.name
