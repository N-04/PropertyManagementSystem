# 文件说明：定义 apps/visitors/models/visitor.py 对应业务的数据模型和数据库映射。

from django.db import models

from apps.owners.models import Owner
from apps.users.models import User


class Visitor(models.Model):
    """
    访客信息表
    用于记录访客预约、审批、到访及离开情况
    """

    STATUS_CHOICES = (
        ("waiting", "待审核"),
        ("approved", "已通过"),
        ("rejected", "已拒绝"),
        ("entered", "已到访"),
        ("left", "已离开"),
    )

    name = models.CharField(max_length=50, verbose_name="访客姓名")

    phone = models.CharField(max_length=20, db_index=True, verbose_name="手机号")

    id_card = models.CharField(
        max_length=18, blank=True, null=True, verbose_name="身份证"
    )

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="被访业主")

    reason = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="来访事由"
    )

    visit_time = models.DateTimeField(verbose_name="来访时间")

    # 到访时间
    enter_time = models.DateTimeField(null=True, blank=True, verbose_name="到访时间")

    # 离开时间
    leave_time = models.DateTimeField(blank=True, null=True, verbose_name="离开时间")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="waiting", verbose_name="状态"
    )

    # 审批时间
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name="审批时间")

    approve_remark = models.CharField(max_length=200, blank=True, null=True)

    # 审批人
    approve_user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="审批人"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "visitor"
        verbose_name = "访客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
