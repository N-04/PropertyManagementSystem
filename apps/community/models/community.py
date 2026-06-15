# 文件说明：定义 apps/community/models/community.py 对应业务的数据模型和数据库映射。

from django.db import models


class Community(models.Model):
    """
    小区表
    """

    # 小区名称
    name = models.CharField(max_length=100, unique=True, verbose_name="小区名称")

    # 小区编码
    code = models.CharField(max_length=50, unique=True, verbose_name="小区编码")

    # 小区地址
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="小区地址"
    )

    # 联系人
    contact_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="联系人"
    )

    # 联系电话
    contact_phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="联系电话"
    )

    # 备注
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "community"
        verbose_name = "小区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
