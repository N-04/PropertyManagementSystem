# 文件说明：定义投诉建议数据模型。
from django.db import models
from django.conf import settings


class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ("complaint", "投诉"),
        ("suggestion", "建议"),
    )

    STATUS_CHOICES = (
        ("pending", "待处理"),
        ("processing", "处理中"),
        ("done", "已完成"),
        ("closed", "已关闭"),
    )

    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="complaint",
        verbose_name="类型",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="状态",
    )
    owner = models.ForeignKey(
        "owners.Owner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="complaints",
        verbose_name="业主",
    )
    phone = models.CharField(max_length=20, blank=True, default="", verbose_name="联系电话")
    handle_result = models.TextField(blank=True, default="", verbose_name="处理结果")
    return_visit = models.TextField(blank=True, default="", verbose_name="回访记录")
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="handled_complaints",
        verbose_name="处理人",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "complaint"
        ordering = ["-id"]
        verbose_name = "投诉建议"
        verbose_name_plural = "投诉建议"

    def __str__(self):
        return self.title
