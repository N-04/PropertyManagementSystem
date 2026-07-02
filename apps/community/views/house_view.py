# 文件说明：处理 apps/community/views/house_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.community.models import House
from apps.community.serializers.house_serializer import HouseSerializer
from apps.logs.services.log_service import save_operation_log
from apps.users.utils.role_access import is_owner_user, is_property_manager_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import (
    ResponseError,
    ResponseSuccess,
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
        keyword = request.GET.get("keyword", "").strip()
        community_id = request.GET.get("community")
        profile_select = request.GET.get("profile_select") in {"1", "true", "True"}
        queryset = House.objects.select_related("unit__building__community").all().order_by("-id")

        if is_owner_user(request.user):
            if profile_select:
                queryset = queryset.filter(
                    Q(status="vacant", owners__isnull=True)
                    | Q(owners__phone=request.user.phone)
                ).distinct()
            else:
                queryset = queryset.filter(owners__phone=request.user.phone).distinct()
        elif not is_property_manager_user(request.user):
            queryset = queryset.none()

        if community_id:
            queryset = queryset.filter(unit__building__community_id=community_id)

        if keyword:
            queryset = queryset.filter(
                Q(room_no__icontains=keyword)
                | Q(house_type__icontains=keyword)
                | Q(status__icontains=keyword)
                | Q(unit__name__icontains=keyword)
                | Q(unit__building__name__icontains=keyword)
                | Q(unit__building__community__name__icontains=keyword)
            )

        # 统一分页会安全处理非法 page/page_size，避免手写 int() 解析导致 500。
        page_queryset, page_meta = paginate_queryset(queryset, request)
        serializer = HouseSerializer(
            page_queryset,
            many=True,
        )

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


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
