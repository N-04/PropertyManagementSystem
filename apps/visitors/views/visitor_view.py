# 文件说明：处理 apps/visitors/views/visitor_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.logs.services.log_service import save_operation_log
from apps.owners.models import Owner
from apps.users.utils.role_access import (
    is_customer_service_user,
    is_owner_user,
    is_property_manager_user,
)
from apps.visitors.models.visitor import Visitor
from apps.visitors.serializers.visitor_serializer import VisitorSerializer
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import ResponseError, ResponseSuccess


def _can_manage_visitor(user):
    """访客通行由物业管理侧和客服侧处理。"""

    return is_property_manager_user(user) or is_customer_service_user(user)


def _owner_for_user(user):
    """按登录用户手机号查找业主资料，业主端数据隔离依赖这个映射。"""

    if not is_owner_user(user) or not getattr(user, "phone", ""):
        return None

    return Owner.objects.filter(phone=user.phone).first()


def _can_access_visitor(user, visitor):
    """校验当前用户是否可以查看指定访客记录。"""

    if _can_manage_visitor(user):
        return True

    # 业主只能访问自己名下的访客，避免看到其他房屋访客记录。
    owner = _owner_for_user(user)
    return bool(owner and visitor.owner_id == owner.id)


class VisitorCreateView(APIView):
    """
    创建访客
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 复制请求体后再补默认字段，避免直接修改 request.data。
        payload = request.data.copy()

        if is_owner_user(request.user):
            owner = _owner_for_user(request.user)

            if not owner:
                return ResponseError(msg="当前账号未绑定业主资料")

            payload["owner"] = owner.id
            payload["status"] = "waiting"
        elif not _can_manage_visitor(request.user):
            return ResponseError(msg="无权创建访客")

        serializer = VisitorSerializer(data=payload)

        if serializer.is_valid():

            serializer.save()

            save_operation_log(
                username=request.user.username,
                module="访客管理",
                action="新增访客",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class VisitorListView(APIView):
    """
    访客列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 筛选参数分块：keyword 做模糊搜索，status 做精确过滤。
        keyword = (request.GET.get("keyword") or "").strip()
        status = (request.GET.get("status") or "").strip()
        queryset = Visitor.objects.select_related("owner", "approve_user").all().order_by("-id")

        # 数据权限分块：业主只看自己的访客，非管理角色不返回访客数据。
        if is_owner_user(request.user):
            owner = _owner_for_user(request.user)
            queryset = queryset.filter(owner=owner) if owner else queryset.none()
        elif not _can_manage_visitor(request.user):
            queryset = queryset.none()

        if keyword:
            # 支持访客、手机号、被访业主和来访事由搜索，供前端列表筛选使用。
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(phone__icontains=keyword)
                | Q(owner__name__icontains=keyword)
                | Q(reason__icontains=keyword)
            )

        if status:
            # 状态筛选下沉到数据库层，避免前端为了筛选而一次性拉取大量访客记录。
            queryset = queryset.filter(status=status)

        # 分页分块：返回 results/count/page，前端表格不再做本地分页。
        page_queryset, page_meta = paginate_queryset(queryset, request)
        serializer = VisitorSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


class VisitorUpdateView(APIView):
    """
    修改访客
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        instance = Visitor.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="访客记录不存在")

        if not _can_manage_visitor(request.user):
            return ResponseError(msg="无权修改访客")

        serializer = VisitorSerializer(
            instance=instance,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            serializer.save()
            save_operation_log(
                username=request.user.username,
                module="访客管理",
                action="处理访客信息",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class VisitorDeleteView(APIView):
    """
    删除访客
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        instance = Visitor.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="访客记录不存在")

        if not _can_manage_visitor(request.user):
            return ResponseError(msg="无权删除访客")

        save_operation_log(
            username=request.user.username,
            module="访客管理",
            action=f"删除访客：{instance.name}",
        )

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class VisitorDetailView(APIView):
    """
    访客详情
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            visitor = Visitor.objects.get(pk=pk)
        except Visitor.DoesNotExist:
            return ResponseError(msg="访客不存在")

        if not _can_access_visitor(request.user, visitor):
            return ResponseError(msg="无权查看访客")

        serializer = VisitorSerializer(visitor)

        return ResponseSuccess(data=serializer.data)


class VisitorApproveView(APIView):
    """
    访客审批
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """
        更新访客审批结果
        """

        # 查询访客
        visitor = Visitor.objects.filter(id=pk).first()

        if not visitor:
            return ResponseError(msg="访客不存在")

        if not _can_manage_visitor(request.user):
            return ResponseError(msg="无权审批访客")

        status = request.data.get("status")

        if status not in {"approved", "rejected"}:
            return ResponseError(msg="审批状态只能为通过或拒绝")

        if visitor.status != "waiting":
            return ResponseError(msg="当前访客不能重复审批")

        # 更新审批状态
        visitor.status = status

        # 更新审批备注
        visitor.approve_remark = request.data.get("approve_remark") or ""

        # 更新审批时间
        visitor.approve_time = timezone.now()

        # 更新审批人
        visitor.approve_user = request.user

        visitor.save(update_fields=["status", "approve_remark", "approve_time", "approve_user"])

        return ResponseSuccess(data=VisitorSerializer(visitor).data, msg="审批成功")


class VisitorEnterView(APIView):
    """
    访客到访登记
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        visitor = Visitor.objects.filter(id=pk).first()

        if not visitor:
            return ResponseError(msg="访客不存在")

        if not _can_manage_visitor(request.user):
            return ResponseError(msg="无权登记访客到访")

        # 必须审批通过才能登记
        if visitor.status != "approved":
            return ResponseError(msg="当前访客不能登记到访")

        visitor.status = "entered"
        visitor.enter_time = timezone.now()

        visitor.save(update_fields=["status", "enter_time"])

        return ResponseSuccess(data=VisitorSerializer(visitor).data, msg="登记成功")


class VisitorLeaveView(APIView):
    """
    登记离开
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        visitor = Visitor.objects.filter(id=pk).first()

        if not visitor:
            return ResponseError(msg="访客不存在")

        if not _can_manage_visitor(request.user):
            return ResponseError(msg="无权登记访客离开")

        if visitor.status != "entered":
            return ResponseError(msg="访客未到访")

        visitor.status = "left"

        visitor.leave_time = timezone.now()

        visitor.save(update_fields=["status", "leave_time"])

        return ResponseSuccess(data=VisitorSerializer(visitor).data, msg="登记成功")
