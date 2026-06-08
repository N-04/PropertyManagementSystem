from django.db import models


class Parking(models.Model):

    owner = models.ForeignKey(
        "owners.Owner",
        on_delete=models.CASCADE,
        related_name="parkings",
        verbose_name="所属业主",
    )

    parking_no = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="车位号",
    )

    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="面积",
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ("idle", "空闲"),
            ("used", "使用中"),
        ),
        default="used",
        verbose_name="状态",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "parking"
