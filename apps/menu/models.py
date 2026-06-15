# 文件说明：社区物业管理系统后端源码文件：apps/menu/models.py。

from django.db import models


class Menu(models.Model):

    name = models.CharField(max_length=50)

    path = models.CharField(max_length=100)

    component = models.CharField(max_length=100)

    parent = models.ForeignKey(
        'self',
        null = True,
        blank = True,
        on_delete = models.CASCADE
    )

    icon = models.CharField(
        max_length = 50,
        null = True,
        blank = True
    )

    class Meta:
        db_table = 'menu'