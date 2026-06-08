# Excel操作
import openpyxl

# Django响应
from django.http import HttpResponse

# DRF
from rest_framework.views import APIView

# 操作日志模型
from apps.logs.models import OperationLog


class OperationLogExportView(APIView):
    """
    操作日志导出Excel
    """

    def get(self, request):

        # 创建工作簿
        workbook = openpyxl.Workbook()

        # 当前工作表
        sheet = workbook.active

        # 表名
        sheet.title = "操作日志"

        # 表头
        sheet.append(
            [
                "ID",
                "用户名",
                "模块",
                "操作内容",
                "操作时间",
            ]
        )

        # 查询数据
        queryset = OperationLog.objects.all().order_by("-id")

        # 写入数据
        for item in queryset:
            sheet.append(
                [
                    item.id,
                    item.username,
                    item.module,
                    item.action,
                    str(item.created_at),
                ]
            )

        # 文件响应
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # 文件名
        response["Content-Disposition"] = 'attachment; filename="operation_log.xlsx"'

        # 保存
        workbook.save(response)

        return response
