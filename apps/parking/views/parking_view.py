# 文件说明：处理 apps/parking/views/parking_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chat.models import ChatConversation, ChatMessage
from apps.finance.models import Fee
from apps.owners.models import Owner
from apps.parking.models import Parking
from apps.parking.serializers.parking_serializer import ParkingSerializer
from apps.users.models import User
from apps.users.utils.role_access import has_any_role, is_owner_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import (
    ResponseError,
    ResponseSuccess,
)
from common.utils.log import save_log

PARKING_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
)
SALE_PARKING_ZONE = "SM"
PARKING_FEE_UNIT_PRICE = Decimal("22.80")
PARKING_FEE_DEFAULT_AMOUNT = Decimal("285.00")
PARKING_FEE_REMARK_PREFIX = "车位费："


# 权限与分区规则分块：车位管理、业主购买和访客临停在这里做边界定义。
def _can_manage_parking(user):
    """车位资料由管理员维护，业主只选择和查看自己的车位。"""

    return has_any_role(user, *PARKING_MANAGE_ROLES) or getattr(user, "is_superuser", False)


def _can_access_parking(user, parking):
    """业主只能访问自己的车位或可选空闲车位，管理员可访问全部。"""

    if _can_manage_parking(user):
        return True

    if is_owner_user(user):
        if parking.owner_id and parking.owner.phone == user.phone:
            return True

        return parking.status == "idle" and not parking.owner_id and _is_sale_parking(parking)

    return False


def _property_admin_queryset():
    """查询可接收车位购买反馈的物业管理员账号。"""

    return User.objects.filter(
        Q(role__code__in=PARKING_MANAGE_ROLES) | Q(roles__code__in=PARKING_MANAGE_ROLES),
        is_active=True,
        status=1,
    ).distinct()


def _is_sale_parking(parking):
    """售卖区车位才允许业主购买；普通区车位保留给访客临停。"""

    return (parking.parking_no or "").strip().upper().startswith(SALE_PARKING_ZONE)


def _parking_fee_amount(parking):
    """根据车位面积生成月度车位费，面积缺失时使用系统默认金额。"""

    if parking.area:
        return (Decimal(parking.area) * PARKING_FEE_UNIT_PRICE).quantize(Decimal("0.01"))

    return PARKING_FEE_DEFAULT_AMOUNT


# 账单联动分块：业主购买车位后需要立刻生成缴费中心可见的车位费。
def _parking_fee_deadline():
    """购买当月 25 日前缴当月费，否则生成下月 25 日截止的车位费。"""

    current = timezone.localtime(timezone.now())
    month_offset = 1 if current.day > 25 else 0
    month_number = current.month - 1 + month_offset
    year = current.year + month_number // 12
    month = month_number % 12 + 1
    naive_deadline = datetime(year, month, 25, 23, 59, 59)

    return timezone.make_aware(naive_deadline, timezone.get_current_timezone())


def _ensure_parking_fee(parking, owner):
    """购置车位后补齐车位费账单，缴费中心才能立即看到待缴费用。"""

    if not owner.house_id:
        return None

    remark = f"{PARKING_FEE_REMARK_PREFIX}{parking.parking_no}"
    existing_fee = (
        Fee.objects.filter(
            owner=owner,
            fee_type="parking",
            remark=remark,
            status__in=("unpaid", "overdue"),
        )
        .order_by("-id")
        .first()
    )

    if existing_fee:
        return existing_fee

    return Fee.objects.create(
        owner=owner,
        house=owner.house,
        fee_type="parking",
        amount=_parking_fee_amount(parking),
        deadline=_parking_fee_deadline(),
        status="unpaid",
        remark=remark,
    )


def _notify_property_admins_for_parking(parking, owner, sender):
    """把业主购买车位事件写入站内会话，确保管理员跨账号也能收到反馈。"""

    if not is_owner_user(sender):
        return None

    admin_users = list(_property_admin_queryset())

    if not admin_users:
        return None

    room_text = owner.house.room_no if owner.house_id else "未绑定房屋"
    title = f"车位购买反馈：{owner.name} {parking.parking_no}"
    content = (
        f"{owner.name} 已成功购买/绑定车位 {parking.parking_no}，"
        f"房号：{room_text}，请物业管理员及时跟进。"
    )
    conversation = ChatConversation.objects.create(
        title=title,
        target_role="property_admin",
        created_by=sender,
        last_message=content,
    )
    conversation.participants.set([sender, *admin_users])
    ChatMessage.objects.create(
        conversation=conversation,
        sender=sender,
        content=content,
        message_type="system",
    )

    return conversation


# 车位接口分块：管理员维护基础资料，业主只能购买售卖区空闲车位。
class ParkingCreateView(APIView):
    """
    创建车位
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not _can_manage_parking(request.user):
            return ResponseError(msg="无权创建车位")

        serializer = ParkingSerializer(data=request.data)

        if serializer.is_valid():

            parking = serializer.save()

            save_log(
                username=request.user.username,
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

    permission_classes = [IsAuthenticated]

    def get(self, request):

        include_idle = request.GET.get("include_idle") in {"1", "true", "True"}
        queryset = Parking.objects.all().order_by("-id")

        # 默认只看“我的车位”；购买页显式 include_idle 时才补充售卖区空闲车位。
        if is_owner_user(request.user):
            owner_filter = Q(owner__phone=request.user.phone)

            if include_idle:
                # 业主选车位时只额外开放售卖区空闲车位，普通区保留给访客临停。
                owner_filter |= Q(
                    owner__isnull=True,
                    status="idle",
                    parking_no__istartswith=SALE_PARKING_ZONE,
                )

            queryset = queryset.filter(owner_filter)
        elif not _can_manage_parking(request.user):
            queryset = queryset.none()

        page_queryset, page_meta = paginate_queryset(queryset, request)
        serializer = ParkingSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


class ParkingBindView(APIView):
    """
    绑定空闲车位
    """

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        parking = Parking.objects.filter(id=pk).first()

        if not parking:
            return ResponseError(msg="车位不存在")

        if parking.status != "idle" or parking.owner_id:
            return ResponseError(msg="该车位已被绑定")

        if not _is_sale_parking(parking):
            return ResponseError(msg="普通区车位仅供访客临停，不支持购买")

        owner = None

        if is_owner_user(request.user):
            # 业主只能把空闲车位绑定到自己的业主资料。
            owner = (
                Owner.objects.filter(phone=request.user.phone)
                .order_by("-is_primary", "-id")
                .first()
            )
        else:
            if not _can_manage_parking(request.user):
                return ResponseError(msg="无权绑定车位")

            owner_id = request.data.get("owner")

            if owner_id:
                owner = Owner.objects.filter(id=owner_id).first()

        if not owner:
            return ResponseError(msg="未找到可绑定的业主信息")

        if not owner.house_id:
            return ResponseError(msg="请先绑定房屋后再购买车位")

        # 车位绑定、账单生成和管理员反馈必须同事务完成，避免出现“有车位但无账单”的半成功状态。
        parking.owner = owner
        parking.status = "used"
        parking.save(update_fields=["owner", "status"])
        parking_fee = _ensure_parking_fee(parking, owner)
        owner_room = owner.house.room_no if owner.house_id else "未绑定房屋"
        feedback_conversation = _notify_property_admins_for_parking(
            parking,
            owner,
            request.user,
        )

        save_log(
            username=getattr(request.user, "username", "system"),
            module="车位管理",
            action=f"业主购买/绑定车位 {parking.parking_no}（业主：{owner.name}，房号：{owner_room}）",
        )

        response_data = ParkingSerializer(parking).data
        response_data["parking_fee_id"] = parking_fee.id if parking_fee else None

        return ResponseSuccess(
            data=response_data,
            msg="车位购买/绑定成功，已反馈管理员" if feedback_conversation else "车位购买/绑定成功",
        )


class ParkingUpdateView(APIView):
    """
    修改车位
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if not _can_manage_parking(request.user):
            return ResponseError(msg="无权修改车位")

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

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        if not _can_manage_parking(request.user):
            return ResponseError(msg="无权删除车位")

        instance = Parking.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="车位不存在")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class ParkingDetailView(APIView):
    """车位详情接口，按角色限制业主只能查看自己或可购买的售卖车位。"""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        instance = Parking.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="车位不存在")

        if not _can_access_parking(request.user, instance):
            return ResponseError(msg="无权查看该车位")

        serializer = ParkingSerializer(instance)

        return ResponseSuccess(data=serializer.data)
