from django.db import models
from apps.owners.models import Owner


class Visitor(models.Model):
    """
    访客
    """

    STATUS_CHOICES = (
        ("waiting", "待到访"),
        ("entered", "已到访"),
        ("left", "已离开"),
    )

    name = models.CharField(max_length=50, verbose_name="访客姓名")

    phone = models.CharField(max_length=20, verbose_name="手机号")

    id_card = models.CharField(
        max_length=18, blank=True, null=True, verbose_name="身份证"
    )

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="被访业主")

    reason = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="来访事由"
    )

    visit_time = models.DateTimeField(verbose_name="来访时间")

    leave_time = models.DateTimeField(blank=True, null=True, verbose_name="离开时间")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="waiting", verbose_name="状态"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "visitor"
        verbose_name = "访客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
