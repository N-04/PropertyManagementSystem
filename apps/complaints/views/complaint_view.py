# 文件说明：处理投诉建议列表、提交、处理和回访接口。
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.complaints.models import Complaint
from apps.complaints.serializers import ComplaintSerializer
from apps.owners.models import Owner
from apps.users.utils.role_access import has_any_role, is_owner_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import ResponseError, ResponseSuccess

COMPLAINT_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
    "customer_service",
    "service",
)


def _can_manage_complaint(user):
    """判断当前用户是否属于投诉建议的后台处理角色。"""
    return has_any_role(user, *COMPLAINT_MANAGE_ROLES) or getattr(user, "is_superuser", False)


def _owner_filter(user):
    """业主视角按绑定业主手机号或提交手机号限定数据范围。"""
    return Q(owner__phone=user.phone) | Q(phone=user.phone)


def _can_owner_access(user, complaint):
    """业主只能访问自己手机号提交或绑定到自己业主档案的记录。"""
    return complaint.phone == user.phone or (
        complaint.owner and complaint.owner.phone == user.phone
    )


def _base_queryset(request):
    """根据角色返回投诉建议基础查询集，后续列表筛选都基于此范围。"""
    queryset = Complaint.objects.select_related("owner", "handler").all()

    if is_owner_user(request.user):
        # 业主端只展示本人的投诉/建议，避免跨业主查看。
        queryset = queryset.filter(_owner_filter(request.user))
    elif not _can_manage_complaint(request.user):
        # 非业主且非管理角色不具备投诉建议列表权限。
        queryset = queryset.none()

    return queryset


class ComplaintListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """按关键词、类型和状态筛选投诉建议列表。"""
        queryset = _base_queryset(request)
        keyword = request.GET.get("keyword")
        category = request.GET.get("category")
        status = request.GET.get("status")

        if keyword:
            # 关键词覆盖标题、内容、业主姓名和联系电话，满足客服快速检索。
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(content__icontains=keyword)
                | Q(owner__name__icontains=keyword)
                | Q(phone__icontains=keyword)
            )

        if category:
            queryset = queryset.filter(category=category)

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.order_by("-id")
        # 列表接口统一分页，避免投诉数据量增长后一次性序列化全集。
        page_queryset, page_meta = paginate_queryset(queryset, request)
        serializer = ComplaintSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


class ComplaintCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """提交投诉建议；业主提交时自动补齐 owner 和手机号。"""
        data = request.data.copy()

        if is_owner_user(request.user):
            owner = Owner.objects.filter(phone=request.user.phone).first()

            if owner:
                # 优先绑定业主档案，方便后台按业主维度跟进。
                data["owner"] = owner.id

            data["phone"] = data.get("phone") or request.user.phone
        elif not _can_manage_complaint(request.user):
            return ResponseError(msg="无权提交投诉")

        serializer = ComplaintSerializer(data=data)

        if not serializer.is_valid():
            return ResponseError(msg="参数错误", data=serializer.errors)

        complaint = serializer.save()
        return ResponseSuccess(data=ComplaintSerializer(complaint).data, msg="提交成功")


class ComplaintDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """查询投诉建议详情，并复用业主/管理端的访问边界。"""
        complaint = get_object_or_404(Complaint, pk=pk)

        if is_owner_user(request.user) and not _can_owner_access(request.user, complaint):
            return ResponseError(msg="无权查看该投诉")

        if not is_owner_user(request.user) and not _can_manage_complaint(request.user):
            return ResponseError(msg="无权查看该投诉")

        return ResponseSuccess(data=ComplaintSerializer(complaint).data)


class ComplaintUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """更新投诉建议；业主只能在待处理阶段修改基础内容。"""
        complaint = get_object_or_404(Complaint, pk=pk)

        if is_owner_user(request.user):
            if not _can_owner_access(request.user, complaint):
                return ResponseError(msg="无权操作该投诉")

            if complaint.status != "pending":
                return ResponseError(msg="已受理的投诉不能修改")

            allowed_fields = {"title", "content", "category", "phone"}
            # 业主端限制可写字段，避免直接修改处理状态或处理结果。
            data = {key: request.data[key] for key in allowed_fields if key in request.data}
        else:
            if not _can_manage_complaint(request.user):
                return ResponseError(msg="无权处理该投诉")

            data = request.data.copy()

        serializer = ComplaintSerializer(complaint, data=data, partial=True)

        if not serializer.is_valid():
            return ResponseError(msg="参数错误", data=serializer.errors)

        # 后台处理时记录当前处理人，业主修改时保留原处理人。
        saved = serializer.save(handler=request.user if not is_owner_user(request.user) else complaint.handler)
        return ResponseSuccess(data=ComplaintSerializer(saved).data, msg="处理成功")


class ComplaintDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """删除投诉建议；业主仅可删除未受理记录，后台角色可按权限删除。"""
        complaint = get_object_or_404(Complaint, pk=pk)

        if is_owner_user(request.user):
            if not _can_owner_access(request.user, complaint):
                return ResponseError(msg="无权删除该投诉")

            if complaint.status != "pending":
                return ResponseError(msg="已受理的投诉不能删除")
        elif not _can_manage_complaint(request.user):
            return ResponseError(msg="无权删除该投诉")

        complaint.delete()
        return ResponseSuccess(msg="删除成功")
