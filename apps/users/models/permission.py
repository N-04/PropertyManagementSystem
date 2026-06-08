from django.db import models

from .menu import Menu

# =====================================================
# 权限表
# =====================================================


class Permission(models.Model):

    # =================================================
    # 权限名称
    # =================================================

    name = models.CharField(max_length=50, verbose_name="权限名称")

    # =================================================
    # 权限编码
    # =================================================

    code = models.CharField(max_length=100, verbose_name="权限编码")

    # =================================================
    # 创建时间
    # =================================================

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    menu = models.ForeignKey(
        Menu, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="菜单"
    )

    class Meta:

        db_table = "sys_permission"

        verbose_name = "权限"

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
