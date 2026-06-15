# 文件说明：定义 apps/users/models/yzxx.py 对应业务的数据模型和数据库映射。

from django.db import models


class OwnerProfile(models.Model):
    """
    业主信息表
    """

    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="owner_profile",
    )

    real_name = models.CharField(
        max_length=20,
        verbose_name="真实姓名",
    )

    id_card = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="身份证",
    )

    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="性别",
    )

    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name="生日",
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="联系地址",
    )

    emergency_contact = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="紧急联系人",
    )

    emergency_phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="紧急联系电话",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "owner_profile"
        verbose_name = "业主信息"
        verbose_name_plural = verbose_name

    # 身份证校验，隐藏中间11位
    @property
    def id_card_mask(self):
        return self.id_card[:3] + "*" * 11 + self.id_card[-4:]
