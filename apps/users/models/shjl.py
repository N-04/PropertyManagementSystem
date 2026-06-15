# 文件说明：定义 apps/users/models/shjl.py 对应业务的数据模型和数据库映射。

class AuditLog(models.Model):

    AUDIT_RESULT = (
        (1, "通过"),
        (2, "拒绝"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    auditor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="audit_users"
    )

    result = models.SmallIntegerField(choices=AUDIT_RESULT)

    remark = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
