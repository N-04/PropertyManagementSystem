# 文件说明：处理 apps/community/views/house_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.community.models import House
from apps.community.serializers.house_serializer import HouseSerializer
from apps.logs.services.log_service import save_operation_log
from apps.users.utils.role_access import is_owner_user, is_property_manager_user
from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log


class HouseCreateView(APIView):
    """
    创建房屋
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权创建房屋")

        serializer = HouseSerializer(data=request.data)

        if serializer.is_valid():
            house = serializer.save()
            save_operation_log(
                username=request.user.username,
                module="房屋管理",
                action=f"新增房屋：{house.room_no}",
            )
            save_log(
                username=request.user.username,
                module="房屋管理",
                action=f"新增房屋 {house.room_no}",
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

    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        keyword = request.GET.get("keyword", "").strip()
        profile_select = request.GET.get("profile_select") in {"1", "true", "True"}
        page = max(page, 1)
        page_size = min(max(page_size, 1), 100)
        queryset = House.objects.select_related("unit__building__community").all().order_by("-id")

        if is_owner_user(request.user):
            owner_filter = Q(owners__phone=request.user.phone)

            if profile_select:
                owner_filter |= Q(owners__isnull=True, status="vacant")

            queryset = queryset.filter(owner_filter).distinct()
        elif not is_property_manager_user(request.user):
            queryset = queryset.none()

        if keyword:
            queryset = queryset.filter(
                Q(room_no__icontains=keyword)
                | Q(house_type__icontains=keyword)
                | Q(status__icontains=keyword)
                | Q(unit__name__icontains=keyword)
                | Q(unit__building__name__icontains=keyword)
                | Q(unit__building__community__name__icontains=keyword)
            )

        total = queryset.count()
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
                "data": {
                    "results": serializer.data,
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                },
            }
        )


class HouseUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权修改房屋")

        instance = House.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="房屋信息不存在")

        serializer = HouseSerializer(
            instance,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            house = serializer.save()
            save_operation_log(
                username=request.user.username,
                module="房屋管理",
                action=f"修改房屋：{house.room_no}",
            )
            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )
        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class HouseDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权删除房屋")

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
            username=request.user.username,
            module="房屋管理",
            action=f"删除房屋 {instance.room_no}",
        )
        return ResponseSuccess(msg="删除成功")
