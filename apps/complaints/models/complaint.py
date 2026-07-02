# 文件说明：定义投诉建议数据模型。
from django.conf import settings
from django.db import models


class Complaint(models.Model):
    """投诉/建议主表，承载业主提交与物业客服处理的完整闭环。"""

    # 类型只区分投诉和建议，前端据此切换入口文案和筛选条件。
    CATEGORY_CHOICES = (
        ("complaint", "投诉"),
        ("suggestion", "建议"),
    )

    # 状态覆盖从提交、处理中到完结/关闭的处理流程。
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
    # owner 允许为空，兼容历史数据或仅通过手机号登记的投诉记录。
    owner = models.ForeignKey(
        "owners.Owner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="complaints",
        verbose_name="业主",
    )
    phone = models.CharField(max_length=20, blank=True, default="", verbose_name="联系电话")
    # 处理结果和回访记录拆开保存，便于后台分别查看处理过程和满意度跟进。
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
        # 新提交的投诉/建议优先展示，方便客服先处理最新问题。
        ordering = ["-id"]
        verbose_name = "投诉建议"
        verbose_name_plural = "投诉建议"

    def __str__(self):
        """后台管理和日志中使用标题快速识别投诉建议。"""
        return self.title
