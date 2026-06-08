from rest_framework.views import APIView

from apps.logs.models.operation_log import OperationLog
from apps.logs.serializers.operation_log_serializer import (
    OperationLogSerializer,
)

from common.response.response import ResponseSuccess


class OperationLogListView(APIView):
    """
    操作日志列表
    """

    def get(self, request):

        queryset = OperationLog.objects.all().order_by("-id")

        serializer = OperationLogSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)
