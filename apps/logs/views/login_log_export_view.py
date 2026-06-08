# Excel操作
import openpyxl

# Django响应
from django.http import HttpResponse

# 登录日志模型
from apps.logs.models import LoginLog

# DRF
from rest_framework.views import APIView


class LoginLogExportView(APIView):
    """
    登录日志导出Excel
    """

    def get(self, request):

        # 创建Excel工作簿
        workbook = openpyxl.Workbook()

        # 获取工作表
        sheet = workbook.active

        # 工作表名称
        sheet.title = "登录日志"

        # 表头
        sheet.append(
            [
                "ID",
                "用户名",
                "IP地址",
                "登录时间",
            ]
        )

        # 查询数据
        queryset = LoginLog.objects.all().order_by("-id")

        # 写入数据
        for item in queryset:

            sheet.append(
                [
                    item.id,
                    item.username,
                    item.ip,
                    str(item.created_at),
                ]
            )

        # 响应对象
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # 下载文件名
        response["Content-Disposition"] = 'attachment; filename="login_log.xlsx"'

        # 保存Excel
        workbook.save(response)

        return response
