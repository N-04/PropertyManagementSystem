# 文件说明：处理 apps/parking/views/parking_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView

from apps.parking.models import Parking
from apps.parking.serializers.parking_serializer import ParkingSerializer
from apps.users.utils.role_access import is_owner_user

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log


class ParkingCreateView(APIView):
    """
    创建车位
    """

    def post(self, request):

        serializer = ParkingSerializer(data=request.data)

        if serializer.is_valid():

            parking = serializer.save()

            save_log(
                username="admin2",
                module="车位管理",
                action=f"新增车位 {parking.parking_no}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class ParkingListView(APIView):
    """
    车位列表
    """

    def get(self, request):

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        queryset = Parking.objects.all().order_by("-id")

        if is_owner_user(request.user):
            queryset = queryset.filter(owner__phone=request.user.phone)
        start = (page - 1) * page_size
        end = start + page_size

        serializer = ParkingSerializer(
            queryset[start:end],
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class ParkingUpdateView(APIView):
    """
    修改车位
    """

    def put(self, request, pk):

        instance = Parking.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="车位不存在")

        serializer = ParkingSerializer(
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


class ParkingDeleteView(APIView):
    """
    删除车位
    """

    def delete(self, request, pk):

        instance = Parking.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="车位不存在")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class ParkingDetailView(APIView):

    def get(self, request, pk):

        instance = Parking.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="车位不存在")

        serializer = ParkingSerializer(instance)

        return ResponseSuccess(data=serializer.data)
