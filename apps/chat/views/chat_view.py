# 文件说明：处理站内即时通讯会话和消息接口。
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chat.models import ChatConversation, ChatMessage
from apps.chat.serializers import ChatConversationSerializer, ChatMessageSerializer
from apps.users.models import User
from apps.users.utils.role_access import get_user_role_codes, has_any_role
from common.response.response import ResponseError, ResponseSuccess


MANAGER_ROLES = {"super_admin", "admin", "property_admin", "customer_service"}
CHAT_TIMEOUT_MINUTES = 5
CHAT_TIMEOUT_MESSAGE = "会话超过5分钟未响应，已自动结束，请对本次服务评分。"
TARGET_ROLE_ALIASES = {
    "customer_service": {"customer_service", "service"},
    "finance_staff": {"finance_staff", "finance"},
    "repair_staff": {"repair_staff", "repairer", "repair"},
    "property_admin": {"property_admin", "admin", "super_admin"},
}


def _user_can_manage_chat(user):
    """管理侧角色可以查看和处理所有会话。"""

    return bool(get_user_role_codes(user) & MANAGER_ROLES)


def _role_user_queryset(role_code):
    """按目标角色找到可参与会话的处理人员账号。"""

    role_codes = TARGET_ROLE_ALIASES.get(role_code, {role_code})

    return User.objects.filter(
        # 角色编码历史上有 finance/finance_staff 等别名，联系对象需要兼容这些账号。
        Q(role__code__in=role_codes) | Q(roles__code__in=role_codes),
        is_active=True,
        status=1,
    ).distinct()


def _conversation_queryset(user):
    """普通用户只看自己发起或参与的会话，管理侧可看全部。"""

    queryset = ChatConversation.objects.prefetch_related(
        "participants",
        "messages__sender",
    ).select_related("created_by")

    if _user_can_manage_chat(user):
        return queryset

    return queryset.filter(Q(created_by=user) | Q(participants=user)).distinct()


def _can_access_conversation(user, conversation):
    """会话访问控制兜底，防止用户通过 id 猜测访问他人会话。"""

    if _user_can_manage_chat(user):
        return True

    if conversation.created_by_id == user.id:
        return True

    return conversation.participants.filter(id=user.id).exists()


def _expire_idle_conversations(queryset=None):
    """懒触发超时结束：访问聊天接口时关闭5分钟未更新的活跃会话。"""

    expire_before = timezone.now() - timedelta(minutes=CHAT_TIMEOUT_MINUTES)

    if queryset is None:
        queryset = ChatConversation.objects.all()

    return queryset.filter(status="active", updated_at__lte=expire_before).update(
        status="resolved",
        end_reason="timeout",
        ended_at=timezone.now(),
        last_message=CHAT_TIMEOUT_MESSAGE,
    )


def _expire_idle_conversation(conversation):
    """单个会话详情/发送消息前的超时兜底。"""

    expire_before = timezone.now() - timedelta(minutes=CHAT_TIMEOUT_MINUTES)

    if conversation.status == "active" and conversation.updated_at <= expire_before:
        conversation.status = "resolved"
        conversation.end_reason = "timeout"
        conversation.ended_at = timezone.now()
        conversation.last_message = CHAT_TIMEOUT_MESSAGE
        conversation.save(update_fields=["status", "end_reason", "ended_at", "last_message"])

    return conversation


def _validate_rating_score(raw_score):
    """评分支持 0.5 分粒度，统一在后端校验防止重复提交异常值。"""

    try:
        score = Decimal(str(raw_score))
    except (InvalidOperation, TypeError, ValueError):
        return None, "评分格式不正确"

    if score < Decimal("0.5") or score > Decimal("5"):
        return None, "评分必须在0.5到5分之间"

    if (score * 2) % 1 != 0:
        return None, "评分必须以0.5分为单位"

    return score, None


class ChatConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 列表查询前先懒清理超时会话，保证状态和评分入口及时更新。
        _expire_idle_conversations(_conversation_queryset(request.user))
        queryset = _conversation_queryset(request.user)
        status = request.GET.get("status")
        target_role = request.GET.get("target_role")
        keyword = request.GET.get("keyword")

        if status:
            queryset = queryset.filter(status=status)

        if target_role:
            queryset = queryset.filter(target_role=target_role)

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(last_message__icontains=keyword)
                | Q(created_by__username__icontains=keyword)
                | Q(created_by__real_name__icontains=keyword)
            )

        serializer = ChatConversationSerializer(queryset, many=True)
        return ResponseSuccess(data=serializer.data)


class ChatConversationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 创建会话时自动拉入目标角色处理人员，也允许前端附加指定参与人。
        serializer = ChatConversationSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseError(msg="参数错误", data=serializer.errors)

        conversation = serializer.save(created_by=request.user)
        participants = {request.user.id}
        target_role = serializer.validated_data["target_role"]

        participants.update(_role_user_queryset(target_role).values_list("id", flat=True))

        for participant_id in request.data.get("participant_ids", []) or []:
            try:
                participants.add(int(participant_id))
            except (TypeError, ValueError):
                return ResponseError(msg="participant_ids 必须是用户ID数组")

        conversation.participants.set(User.objects.filter(id__in=participants))

        content = (request.data.get("content") or "").strip()

        if content:
            # 首条内容同步写入 last_message，列表页不用再额外查询消息表。
            ChatMessage.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
            )
            conversation.last_message = content
            conversation.save(update_fields=["last_message", "updated_at"])

        return ResponseSuccess(data=ChatConversationSerializer(conversation).data, msg="会话创建成功")


class ChatConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 详情接口需要预取消息和发送人，避免序列化时重复查库。
        conversation = get_object_or_404(
            ChatConversation.objects.prefetch_related("participants", "messages__sender"),
            pk=pk,
        )

        if not _can_access_conversation(request.user, conversation):
            return ResponseError(msg="无权查看该会话")

        conversation = _expire_idle_conversation(conversation)

        return ResponseSuccess(data=ChatConversationSerializer(conversation).data)


class ChatMessageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 只有活跃会话允许继续发送消息，超时或手动结束后转为评分流程。
        conversation = get_object_or_404(ChatConversation, pk=pk)

        if not _can_access_conversation(request.user, conversation):
            return ResponseError(msg="无权发送该会话消息")

        conversation = _expire_idle_conversation(conversation)

        if conversation.status != "active":
            return ResponseError(msg="会话已结束，请对本次服务评分")

        content = (request.data.get("content") or "").strip()

        if not content:
            return ResponseError(msg="消息内容不能为空")

        message = ChatMessage.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
        )
        conversation.last_message = content
        conversation.participants.add(request.user)
        conversation.save(update_fields=["last_message", "updated_at"])

        return ResponseSuccess(data=ChatMessageSerializer(message).data, msg="发送成功")


class ChatConversationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # 管理人员手动结束会话时记录结束原因和时间，重新激活时清空结束态。
        conversation = get_object_or_404(ChatConversation, pk=pk)

        if not _can_access_conversation(request.user, conversation):
            return ResponseError(msg="无权操作该会话")

        status = request.data.get("status")
        valid_status = {choice[0] for choice in ChatConversation.STATUS_CHOICES}

        if status not in valid_status:
            return ResponseError(msg="会话状态不正确")

        conversation.status = status

        if status == "active":
            conversation.end_reason = None
            conversation.ended_at = None
            update_fields = ["status", "end_reason", "ended_at", "updated_at"]
        else:
            conversation.end_reason = "manual"
            conversation.ended_at = conversation.ended_at or timezone.now()
            update_fields = ["status", "end_reason", "ended_at", "updated_at"]

        conversation.save(update_fields=update_fields)

        return ResponseSuccess(data=ChatConversationSerializer(conversation).data, msg="状态已更新")


class ChatConversationRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 评分只允许会话发起人提交一次，避免处理人员或重复弹窗二次评分。
        conversation = get_object_or_404(ChatConversation, pk=pk)

        if conversation.created_by_id != request.user.id:
            return ResponseError(msg="只有会话发起人可以评分")

        conversation = _expire_idle_conversation(conversation)

        if conversation.status == "active":
            return ResponseError(msg="会话结束后才能评分")

        if conversation.rating_score is not None or conversation.rating_at:
            return ResponseError(msg="该会话已评分，不能重复提交")

        score, error = _validate_rating_score(request.data.get("rating_score"))

        if error:
            return ResponseError(msg=error)

        rating_comment = (request.data.get("rating_comment") or "").strip()

        if len(rating_comment) > 500:
            return ResponseError(msg="评价内容不能超过500字")

        conversation.rating_score = score
        conversation.rating_comment = rating_comment
        conversation.rating_at = timezone.now()
        conversation.save(update_fields=["rating_score", "rating_comment", "rating_at"])

        feedback_message = f"用户已提交服务评分：{score}分"

        if rating_comment:
            feedback_message = f"{feedback_message}，评价：{rating_comment}"

        # 评分结果写入会话系统消息，相关处理人员刷新列表后也能看到反馈。
        ChatMessage.objects.create(
            conversation=conversation,
            sender=request.user,
            content=feedback_message,
            message_type="system",
        )
        conversation.last_message = feedback_message
        conversation.save(update_fields=["last_message", "updated_at"])

        return ResponseSuccess(data=ChatConversationSerializer(conversation).data, msg="评分成功")
