# 文件说明：处理 apps/finance/views/fee_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.finance.models import Fee
from apps.finance.serializers.fee_serializer import FeeSerializer
from apps.users.utils.role_access import has_any_role, is_owner_user

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log
from apps.logs.services.log_service import save_operation_log


FEE_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
    "finance_staff",
    "finance",
)
FEE_CREATE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
)


def _can_create_fee(user):
    """新增账单只开放给管理员和物业管理员，财务人员负责查看和维护已有账单。"""

    return has_any_role(user, *FEE_CREATE_ROLES) or getattr(user, "is_superuser", False)


def _can_manage_fee(user):
    """收费账单由管理员和财务人员维护，业主只负责查看和支付自己的账单。"""

    return has_any_role(user, *FEE_MANAGE_ROLES) or getattr(user, "is_superuser", False)


def _parse_query_date(raw_value):
    """兼容日期选择器和接口客户端传入的日期格式。"""

    parsed_date = parse_date(raw_value)

    if parsed_date:
        return parsed_date

    parsed_datetime = parse_datetime(raw_value)

    if parsed_datetime:
        return parsed_datetime.date()

    return None


class FeeCreateView(APIView):
    """
    新增收费
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not _can_create_fee(request.user):
            return ResponseError(msg="财务人员无权新增账单")

        serializer = FeeSerializer(data=request.data)

        if serializer.is_valid():

            fee = serializer.save()
            save_operation_log(
                username=request.user.username,
                module="物业费管理",
                action=f"新增账单：{fee.amount}元",
            )
            save_log(
                username=request.user.username,
                module="收费管理",
                action=f"新增收费 {fee.amount}",
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

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = Fee.objects.all().order_by("-id")

        if is_owner_user(request.user):
            queryset = queryset.filter(owner__phone=request.user.phone)

        keyword = request.GET.get("keyword", "").strip()
        fee_type = request.GET.get("fee_type", "").strip()
        date_from_raw = (
            request.GET.get("date_from") or request.GET.get("start_date") or ""
        ).strip()
        date_to_raw = (
            request.GET.get("date_to") or request.GET.get("end_date") or ""
        ).strip()

        if keyword:
            queryset = queryset.filter(
                Q(owner__name__icontains=keyword)
                | Q(owner__phone__icontains=keyword)
                | Q(house__room_no__icontains=keyword)
                | Q(house__unit__name__icontains=keyword)
                | Q(house__unit__building__name__icontains=keyword)
                | Q(remark__icontains=keyword)
            )

        if fee_type:
            valid_fee_types = {choice[0] for choice in Fee.TYPE_CHOICES}

            if fee_type not in valid_fee_types:
                return ResponseError(msg="费用类型不正确")

            queryset = queryset.filter(fee_type=fee_type)

        if date_from_raw:
            date_from = _parse_query_date(date_from_raw)

            if not date_from:
                return ResponseError(msg="开始日期格式不正确")

            queryset = queryset.filter(deadline__date__gte=date_from)

        if date_to_raw:
            date_to = _parse_query_date(date_to_raw)

            if not date_to:
                return ResponseError(msg="结束日期格式不正确")

            queryset = queryset.filter(deadline__date__lte=date_to)

        serializer = FeeSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class FeeUpdateView(APIView):
    """
    修改物业费
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if not _can_manage_fee(request.user):
            return ResponseError(msg="无权修改账单")

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

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        if not _can_manage_fee(request.user):
            return ResponseError(msg="无权删除账单")

        instance = Fee.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="物业费记录不存在")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class FeePayView(APIView):
    """
    缴费
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        fee = Fee.objects.filter(id=pk).first()

        if not fee:
            return ResponseError(msg="账单不存在")

        if not is_owner_user(request.user):
            return ResponseError(msg="仅业主可以缴纳账单")

        if fee.owner.phone != request.user.phone:
            return ResponseError(msg="无权操作该账单")

        if fee.status == "paid":
            return ResponseError(msg="账单已缴费")

        payment_method = request.data.get("payment_method")
        valid_methods = {choice[0] for choice in Fee.PAYMENT_METHOD_CHOICES}

        if payment_method not in valid_methods:
            return ResponseError(msg="请选择正确的支付方式")

        fee.status = "paid"
        fee.pay_time = timezone.now()
        fee.payment_method = payment_method

        fee.save(update_fields=["status", "pay_time", "payment_method"])

        save_log(
            username=request.user.username,
            module="收费管理",
            action=f"缴费账单 {fee.id}",
        )

        return ResponseSuccess(data=FeeSerializer(fee).data, msg="缴费成功")
