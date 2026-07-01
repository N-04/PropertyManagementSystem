# 文件说明：处理 apps/finance/views/fee_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chat.models import ChatConversation, ChatMessage
from apps.chat.serializers import ChatConversationSerializer
from apps.finance.models import Fee
from apps.finance.serializers.fee_serializer import FeeSerializer
from apps.logs.services.log_service import save_operation_log
from apps.owners.services.owner_account_service import ensure_owner_login_user
from apps.users.utils.role_access import has_any_role, is_owner_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import (
    ResponseError,
    ResponseSuccess,
)
from common.utils.log import save_log

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


# 财务权限分块：新增、维护和业主支付分开判断，避免财务代替业主付款。
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


def _fee_type_text(fee):
    """把账单费用类型转为面向用户的中文文案。"""

    return dict(Fee.TYPE_CHOICES).get(fee.fee_type, fee.fee_type)


def _format_fee_deadline(deadline):
    """把截止时间格式化为提醒消息中的简短中文时间。"""

    if not deadline:
        return "-"

    return timezone.localtime(deadline).strftime("%Y-%m-%d %H:%M")


# 账单接口分块：列表、支付和提醒都复用同一套费用模型。
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

        # 基础查询带上业主、房屋、楼栋等关系，避免列表序列化时反复查库。
        queryset = (
            Fee.objects.select_related(
                "owner",
                "house",
                "house__unit",
                "house__unit__building",
            )
            .all()
            .order_by("-id")
        )

        # 业主只能查看自己的账单；财务和管理员可以查看待处理账单池。
        if is_owner_user(request.user):
            queryset = queryset.filter(owner__phone=request.user.phone)
        elif not _can_manage_fee(request.user):
            queryset = queryset.none()

        keyword = request.GET.get("keyword", "").strip()
        fee_type = request.GET.get("fee_type", "").strip()
        status = request.GET.get("status", "").strip()
        date_from_raw = (
            request.GET.get("date_from") or request.GET.get("start_date") or ""
        ).strip()
        date_to_raw = (
            request.GET.get("date_to") or request.GET.get("end_date") or ""
        ).strip()

        # 筛选分块：先按关键字/类型/状态/日期收窄，再统一分页返回。
        # 搜索覆盖业主、手机号、房号和备注，匹配前端统一搜索框。
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
            # 费用类型必须落在模型枚举内，防止随意传参造成无意义筛选。
            valid_fee_types = {choice[0] for choice in Fee.TYPE_CHOICES}

            if fee_type not in valid_fee_types:
                return ResponseError(msg="费用类型不正确")

            queryset = queryset.filter(fee_type=fee_type)

        if status:
            # 缴费记录页通过 status=paid 获取已缴费订单，未缴费页不混入已支付数据。
            valid_statuses = {choice[0] for choice in Fee.STATUS_CHOICES}

            if status not in valid_statuses:
                return ResponseError(msg="缴费状态不正确")

            queryset = queryset.filter(status=status)

        if date_from_raw:
            date_from = _parse_query_date(date_from_raw)

            if not date_from:
                return ResponseError(msg="开始日期格式不正确")

            # 日期筛选基于账单截止日，符合财务“到期账单”查询语义。
            queryset = queryset.filter(deadline__date__gte=date_from)

        if date_to_raw:
            date_to = _parse_query_date(date_to_raw)

            if not date_to:
                return ResponseError(msg="结束日期格式不正确")

            # 结束日期按自然日包含当天，避免前端日期控件选择当天却查不到数据。
            queryset = queryset.filter(deadline__date__lte=date_to)

        page_queryset, page_meta = paginate_queryset(
            queryset,
            request,
            default_page_size=10,
            max_page_size=100,
        )
        serializer = FeeSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


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

        # 支付动作只允许账单所属业主执行，管理员和财务不能代替业主付款。
        fee = (
            Fee.objects.select_related(
                "owner",
                "house",
                "house__unit",
                "house__unit__building",
            )
            .filter(id=pk)
            .first()
        )

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

        # 支付成功后立即落库，业主缴费中心和财务工作台会通过实时刷新同步变化。
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


class FeeReminderView(APIView):
    """
    发送缴费提醒给账单对应业主。
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        # 提醒会写入角色消息中心，而不是跳转到欠费列表。
        if not _can_manage_fee(request.user):
            return ResponseError(msg="无权发送缴费提醒")

        fee = (
            Fee.objects.select_related(
                "owner",
                "house",
                "house__unit",
                "house__unit__building",
            )
            .filter(id=pk)
            .first()
        )

        if not fee:
            return ResponseError(msg="账单不存在")

        if fee.status == "paid":
            return ResponseError(msg="账单已缴费，无需提醒")

        owner_user, owner_user_created = ensure_owner_login_user(fee.owner)

        if not owner_user:
            return ResponseError(msg="未找到该业主对应登录账号")

        # 提醒消息落到业主消息中心，财务端只返回发送结果和会话摘要。
        # 将账单信息组装成面向业主的站内信内容。
        fee_type = _fee_type_text(fee)
        room_parts = [
            fee.house.unit.building.name if fee.house and fee.house.unit else "",
            fee.house.unit.name if fee.house and fee.house.unit else "",
            fee.house.room_no if fee.house else "",
        ]
        room_text = "-".join([item for item in room_parts if item]) or "对应房屋"
        title = f"缴费提醒：{fee.owner.name}{fee_type}#{fee.id}"
        content = (
            f"您有一笔{fee_type}待缴，房屋：{room_text}，"
            f"金额：{fee.amount}元，截止时间：{_format_fee_deadline(fee.deadline)}。"
            "请及时在缴费中心处理。"
        )

        conversation = (
            ChatConversation.objects.filter(
                title=title,
                target_role="owner",
                participants=owner_user,
            )
            .order_by("-updated_at", "-id")
            .first()
        )

        # 同一账单提醒复用会话，避免财务人员多次点击后生成一堆重复会话。
        if not conversation:
            conversation = ChatConversation.objects.create(
                title=title,
                target_role="owner",
                created_by=request.user,
            )
            conversation.participants.set([request.user, owner_user])
        else:
            # 结束过的会话被再次提醒时重新激活，让业主仍从同一消息线程看到最新提醒。
            conversation.status = "active"
            conversation.end_reason = None
            conversation.ended_at = None
            conversation.participants.add(request.user, owner_user)

        ChatMessage.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
            message_type="system",
        )

        conversation.last_message = content
        conversation.save(update_fields=["status", "end_reason", "ended_at", "last_message", "updated_at"])

        save_operation_log(
            username=request.user.username,
            module="缴费提醒",
            action=f"发送账单 {fee.id} 提醒给 {fee.owner.name}",
        )
        save_log(
            username=request.user.username,
            module="收费管理",
            action=f"提醒账单 {fee.id}（业主账号{'已自动补齐' if owner_user_created else '已存在'}）",
        )

        return ResponseSuccess(
            data=ChatConversationSerializer(conversation).data,
            msg="提醒已发送给业主",
        )
