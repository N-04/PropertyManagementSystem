# 文件说明：处理 apps/parking/views/parking_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chat.models import ChatConversation, ChatMessage
from apps.parking.models import Parking
from apps.parking.serializers.parking_serializer import ParkingSerializer
from apps.owners.models import Owner
from apps.users.models import User
from apps.users.utils.role_access import has_any_role, is_owner_user

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log


PARKING_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
)
SALE_PARKING_PREFIX = "SM-"


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

        return parking.status == "idle" and not parking.owner_id

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

    return (parking.parking_no or "").upper().startswith(SALE_PARKING_PREFIX)


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

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        include_idle = request.GET.get("include_idle") in {"1", "true", "True"}
        queryset = Parking.objects.all().order_by("-id")

        if is_owner_user(request.user):
            owner_filter = Q(owner__phone=request.user.phone)

            if include_idle:
                # 业主选车位时只额外开放售卖区空闲车位，普通区保留给访客临停。
                owner_filter |= Q(
                    owner__isnull=True,
                    status="idle",
                    parking_no__istartswith=SALE_PARKING_PREFIX,
                )

            queryset = queryset.filter(owner_filter)
        elif not _can_manage_parking(request.user):
            queryset = queryset.none()
        start = (page - 1) * page_size
        end = start + page_size

        serializer = ParkingSerializer(
            queryset[start:end],
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class ParkingBindView(APIView):
    """
    绑定空闲车位
    """

    permission_classes = [IsAuthenticated]

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

        parking.owner = owner
        parking.status = "used"
        parking.save(update_fields=["owner", "status"])
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

        return ResponseSuccess(
            data=ParkingSerializer(parking).data,
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

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        instance = Parking.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="车位不存在")

        if not _can_access_parking(request.user, instance):
            return ResponseError(msg="无权查看该车位")

        serializer = ParkingSerializer(instance)

        return ResponseSuccess(data=serializer.data)
