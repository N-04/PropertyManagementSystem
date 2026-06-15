# 文件说明：处理 apps/community/views/house_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from turtledemo.penrose import start

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.community.models import House
from apps.community.serializers.house_serializer import HouseSerializer
from apps.logs.services.log_service import save_operation_log
from apps.users.utils.role_access import is_owner_user
from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log


class HouseCreateView(APIView):
    """
    创建房屋
    """

    def post(self, request):

        serializer = HouseSerializer(data=request.data)

        if serializer.is_valid():
            house = serializer.save()
            save_operation_log(
                username=request.user.username,
                module="房屋管理",
                action=f"新增房屋：{house.room_no}",
            )
            save_log(
                username="admin2", module="房屋管理", action=f"新增房屋 {house.room_no}"
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class HouseListView(APIView):
    """
    房屋列表
    """

    def get(self, request):
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        queryset = House.objects.all().order_by("-id")

        if is_owner_user(request.user):
            queryset = queryset.filter(owners__phone=request.user.phone).distinct()
        start = (page - 1) * page_size
        end = start + page_size

        serializer = HouseSerializer(
            queryset[start:end],
            many=True,
        )

        return Response(
            {
                "code": 200,
                "msg": "success",
                "data": serializer.data,
            }
        )


class HouseUpdateView(APIView):
    def put(self, request):
        serializer = HouseSerializer(data=request.data)
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


class HouseDeleteView(APIView):
    def delete(self, request, pk):
        instance = House.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="房屋信息不存在")

        save_operation_log(
            username=request.user.username,
            module="房屋管理",
            action=f"删除房屋：{instance.room_no}",
        )
        instance.delete()
        save_log(
            username="admin2",
            module="房屋管理",
            action=f"删除房屋 {instance.room_no}",
        )
        return ResponseSuccess(msg="删除成功")
