from rest_framework.views import APIView

from apps.finance.models import Fee
from apps.finance.serializers.fee_serializer import FeeSerializer

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log
from apps.logs.services.log_service import save_operation_log


class FeeCreateView(APIView):
    """
    新增收费
    """

    def post(self, request):

        serializer = FeeSerializer(data=request.data)

        if serializer.is_valid():

            fee = serializer.save()
            save_operation_log(
                username=request.user.username,
                module="物业费管理",
                action=f"缴费成功：{fee.amount}元",
            )
            save_log(
                username="admin2",
                module="收费管理",
                action=f"新增收费 {fee.amount}",
            )
            save_log(
                username="admin2",
                module="收费管理",
                action=f"收费缴费 {fee.id}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class FeeListView(APIView):
    """
    物业费列表
    """

    def get(self, request):

        queryset = Fee.objects.all().order_by("-id")

        serializer = FeeSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class FeeUpdateView(APIView):
    """
    修改物业费
    """

    def put(self, request, pk):

        instance = Fee.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="物业费记录不存在")

        serializer = FeeSerializer(
            instance=instance,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            serializer.save()

            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class FeeDeleteView(APIView):
    """
    删除物业费
    """

    def delete(self, request, pk):

        instance = Fee.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="物业费记录不存在")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class FeePayView(APIView):
    """
    缴费
    """

    def put(self, request, pk):

        fee = Fee.objects.filter(id=pk).first()

        if not fee:
            return ResponseError(msg="账单不存在")

        fee.status = "paid"

        fee.save()

        save_log(
            username="admin2",
            module="收费管理",
            action=f"缴费账单 {fee.id}",
        )

        return ResponseSuccess(msg="缴费成功")
