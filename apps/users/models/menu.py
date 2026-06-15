# 文件说明：定义 apps/users/models/menu.py 对应业务的数据模型和数据库映射。

from django.db import models


class Menu(models.Model):

    title = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="菜单名称"
    )

    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name="图标")

    path = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="路由地址"
    )

    component = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="前端组件"
    )

    sort = models.IntegerField(default=0, null=True, blank=True, verbose_name="排序")

    hidden = models.BooleanField(
        default=False, null=True, blank=True, verbose_name="是否隐藏"
    )

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父菜单"
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    menu_type = models.IntegerField(default=1, verbose_name="菜单类型")

    class Meta:
        db_table = "menu"
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
