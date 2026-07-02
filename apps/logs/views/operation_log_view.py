# 文件说明：处理 apps/logs/views/operation_log_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.logs.models.operation_log import OperationLog
from apps.logs.serializers.operation_log_serializer import (
    OperationLogSerializer,
)
from apps.users.utils.role_access import is_property_manager_user
from common.response.response import ResponseError, ResponseSuccess


class OperationLogListView(APIView):
    """
    操作日志列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权查看操作日志")

        queryset = OperationLog.objects.all().order_by("-id")

        serializer = OperationLogSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)
