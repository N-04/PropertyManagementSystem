# 文件说明：处理 apps/owners/views/owner_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

import re

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.logs.services.log_service import save_operation_log
from apps.owners.models import Owner
from apps.owners.serializers.owner_serializer import OwnerSerializer
from apps.owners.services.owner_account_service import ensure_owner_login_user
from apps.users.utils.role_access import has_any_role, is_owner_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import (
    ResponseError,
    ResponseSuccess,
)
from common.utils.log import save_log

OWNER_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
)


# 业主权限分块：管理员维护业主档案，业主本人只读自己的资料。
def _can_manage_owner(user):
    """业主资料由管理员维护，业主只能查看自己的资料。"""

    return has_any_role(user, *OWNER_MANAGE_ROLES) or getattr(user, "is_superuser", False)


def _can_access_owner(user, owner):
    """校验单条业主资料访问权，避免详情接口暴露其他业主身份证和手机号。"""

    if _can_manage_owner(user):
        return True

    return is_owner_user(user) and owner.phone == user.phone


class OwnerCreateView(APIView):
    """
    创建业主
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _can_manage_owner(request.user):
            return ResponseError(msg="无权创建业主")

        id_card = request.data.get("id_card") or ""
        pattern = r"^\d{17}[\dXx]$"

        if not re.match(pattern, id_card):
            return ResponseError(msg="身份证格式错误")

        serializer = OwnerSerializer(data=request.data)

        if serializer.is_valid():
            house = serializer.validated_data["house"]

            if serializer.validated_data.get("is_primary"):

                exists = Owner.objects.filter(
                    house=house,
                    is_primary=True,
                ).exists()

                if exists:
                    return ResponseError(msg="该房屋已有主业主")

            owner = serializer.save()
            ensure_owner_login_user(owner)

            # 记录操作日志
            save_operation_log(
                username=request.user.username,
                module="业主管理",
                action=f"新增业主：{serializer.validated_data.get('name')}",
            )

            save_log(
                username=request.user.username,
                module="业主管理",
                action=f"新增业主 {owner.name}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class OwnerListView(APIView):
    """
    业主列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        keyword = request.GET.get("keyword")
        queryset = Owner.objects.select_related(
            "house__unit__building__community"
        ).order_by("-id")

        # 业主列表先按身份收窄，再执行关键字搜索和分页，避免搜索其他业主资料。
        if is_owner_user(request.user):
            queryset = queryset.filter(phone=request.user.phone)
        elif not _can_manage_owner(request.user):
            queryset = queryset.none()

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(phone__icontains=keyword)
            )

        page_queryset, page_meta = paginate_queryset(queryset, request)
        serializer = OwnerSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


class OwnerUpdateView(APIView):
    """
    修改业主
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return ResponseError(msg="业主不存在")

        if not _can_manage_owner(request.user):
            return ResponseError(msg="无权修改业主")

        if request.data.get("id_card"):
            pattern = r"^\d{17}[\dXx]$"

            id_card = request.data.get("id_card")

            if not id_card:
                return ResponseError(msg="身份证不能为空")

            # 这里只做轻量格式校验，完整身份证规则由注册/认证流程负责。
            if not re.match(pattern, id_card):
                return ResponseError(msg="身份证格式错误")

        serializer = OwnerSerializer(
            owner,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            if serializer.validated_data.get("is_primary"):

                house = serializer.validated_data.get(
                    "house",
                    owner.house,
                )

                exists = (
                    Owner.objects.filter(
                        house=house,
                        is_primary=True,
                    )
                    .exclude(
                        id=owner.id,
                    )
                    .exists()
                )

                if exists:
                    return ResponseError(msg="该房屋已有主业主")

            instance = Owner.objects.filter(id=pk).first()
            owner = serializer.save()
            ensure_owner_login_user(owner)
            save_operation_log(
                username=request.user.username,
                module="业主管理",
                action=f"修改业主：{instance.name}",
            )
            save_log(
                username=request.user.username,
                module="业主管理",
                action=f"修改业主 {owner.name}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class OwnerDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # 删除前先取对象，保证不存在和无权限两类错误能给出明确提示。
        instance = Owner.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="业主不存在")

        if not _can_manage_owner(request.user):
            return ResponseError(msg="无权删除业主")

        save_operation_log(
            username=request.user.username,
            module="业主管理",
            action=f"删除业主：{instance.name}",
        )
        save_log(
            username=request.user.username,
            module="业主管理",
            action=f"删除业主 {instance.name}",
        )

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class OwnerDetailView(APIView):
    """
    业主详情
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return ResponseError(msg="业主不存在")

        if not _can_access_owner(request.user, owner):
            return ResponseError(msg="无权查看该业主")

        serializer = OwnerSerializer(owner)

        return ResponseSuccess(data=serializer.data)
