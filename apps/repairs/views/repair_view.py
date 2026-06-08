from rest_framework.views import APIView

from apps.repairs.models import Repair
from apps.repairs.serializers.repair_serializer import RepairSerializer

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from apps.logs.services.log_service import save_operation_log


class RepairCreateView(APIView):
    """
    创建报修
    """

    def post(self, request):

        serializer = RepairSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            save_operation_log(
                username=request.user.username,
                module="报修管理",
                action="新增报修",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class RepairListView(APIView):
    """
    报修列表
    """

    def get(self, request):

        queryset = Repair.objects.all().order_by("-id")

        serializer = RepairSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class RepairUpdateView(APIView):
    """
    修改报修
    """

    def put(self, request, pk):

        instance = Repair.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="报修记录不存在")

        serializer = RepairSerializer(
            instance=instance,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            serializer.save()
            save_operation_log(
                username=request.user.username,
                module="报修管理",
                action="处理报修",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class RepairDeleteView(APIView):
    """
    删除报修
    """

    def delete(self, request, pk):

        instance = Repair.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="报修记录不存在")

        instance.delete()

        return ResponseSuccess(msg="删除成功")
