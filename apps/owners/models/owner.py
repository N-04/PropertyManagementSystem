from django.db import models


class Owner(models.Model):
    """
    业主
    """

    house = models.ForeignKey(
        "community.House",
        on_delete=models.CASCADE,
        related_name="owners",
        verbose_name="所属房屋",
    )

    name = models.CharField(
        max_length=50,
        verbose_name="姓名",
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="手机号",
    )

    # 头像
    avatar = models.ImageField(
        upload_to="owner/", null=True, blank=True, verbose_name="头像"
    )

    relationship = models.CharField(
        max_length=20,
        choices=(
            ("self", "本人"),
            ("spouse", "配偶"),
            ("child", "子女"),
            ("parent", "父母"),
            ("other", "其他"),
        ),
        default="self",
        verbose_name="与主业主关系",
    )

    # 身份证号
    id_card = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="身份证号",
    )

    # 身份证照片
    id_card_image = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="身份证照片",
    )

    gender = models.CharField(
        max_length=10,
        choices=(
            ("male", "男"),
            ("female", "女"),
        ),
        default="male",
        verbose_name="性别",
    )

    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name="出生日期",
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="是否主业主",
    )

    remark = models.TextField(
        null=True,
        blank=True,
        verbose_name="备注",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "owner"

    def __str__(self):
        return self.name
