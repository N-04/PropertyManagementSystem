# 文件说明：处理 apps/notice/views/notice_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.notice.models import Notice
from apps.notice.serializers.notice_serializer import NoticeSerializer
from apps.users.utils.role_access import has_any_role
from common.response.response import (
    ResponseError,
    ResponseSuccess,
)
from common.utils.log import save_log

NOTICE_PUBLISH_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
    "finance_staff",
    "finance",
    "repair_staff",
    "repairer",
    "repair",
)
NOTICE_ADMIN_ROLES = ("admin", "super_admin", "property_admin")
NOTICE_FINANCE_ROLES = ("finance_staff", "finance")
NOTICE_REPAIR_ROLES = ("repair_staff", "repairer", "repair")


def _can_publish_notice(user):
    """管理员、财务和维修角色可以发布相关公告；业主和客服不可发布。"""

    return has_any_role(user, *NOTICE_PUBLISH_ROLES) or getattr(user, "is_superuser", False)


def _is_notice_admin(user):
    return has_any_role(user, *NOTICE_ADMIN_ROLES) or getattr(user, "is_superuser", False)


def _notice_type_scope(user):
    """按角色限定公告类型：财务只处理财务公告，维修只处理维修公告。"""

    if _is_notice_admin(user):
        return {choice[0] for choice in Notice.TYPE_CHOICES}

    if has_any_role(user, *NOTICE_FINANCE_ROLES):
        return {"finance"}

    if has_any_role(user, *NOTICE_REPAIR_ROLES):
        return {"repair"}

    if has_any_role(user, "owner"):
        return {choice[0] for choice in Notice.TYPE_CHOICES}

    return set()


def _normalize_notice_type(request, user, existing_type=None):
    allowed_types = _notice_type_scope(user)
    notice_type = request.data.get("notice_type")

    if not notice_type and existing_type:
        notice_type = existing_type
    elif not notice_type and allowed_types:
        # 财务和维修发布入口固定类型；管理员未选择时默认系统公告。
        notice_type = "general" if _is_notice_admin(user) else next(iter(allowed_types))

    if notice_type not in allowed_types:
        return None, ResponseError(msg="当前角色无权发布该类型公告")

    data = request.data.copy()
    data["notice_type"] = notice_type

    return data, None


def _can_manage_notice_instance(user, notice):
    return notice.notice_type in _notice_type_scope(user) and _can_publish_notice(user)


def _can_access_notice(user):
    """公告列表开放给接收方业主、管理员以及发布方财务/维修。"""

    return _can_publish_notice(user) or has_any_role(user, "owner")


class NoticeCreateView(APIView):
    """
    创建公告
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not _can_publish_notice(request.user):
            return ResponseError(msg="无权发布公告")

        data, error = _normalize_notice_type(request, request.user)

        if error:
            return error

        serializer = NoticeSerializer(data=data)

        if serializer.is_valid():

            notice = serializer.save()

            save_log(
                username=request.user.username,
                module="公告管理",
                action=f"新增公告 {notice.title}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class NoticeListView(APIView):
    """
    公告列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not _can_access_notice(request.user):
            return ResponseError(msg="无权查看公告")

        queryset = Notice.objects.all().order_by("-id")

        allowed_types = _notice_type_scope(request.user)

        if not allowed_types:
            return ResponseError(msg="无权查看公告")

        queryset = queryset.filter(notice_type__in=allowed_types)

        if not _can_publish_notice(request.user):
            # 业主是公告接收方，只能看到已发布公告，不能看到草稿。
            queryset = queryset.filter(status="published")

        serializer = NoticeSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class NoticeUpdateView(APIView):
    """
    修改公告
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if not _can_publish_notice(request.user):
            return ResponseError(msg="无权修改公告")

        instance = Notice.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="公告不存在")

        if not _can_manage_notice_instance(request.user, instance):
            return ResponseError(msg="无权修改该类型公告")

        data, error = _normalize_notice_type(
            request,
            request.user,
            existing_type=instance.notice_type,
        )

        if error:
            return error

        serializer = NoticeSerializer(
            instance=instance,
            data=data,
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


class NoticeDeleteView(APIView):
    """
    删除公告
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        if not _can_publish_notice(request.user):
            return ResponseError(msg="无权删除公告")

        instance = Notice.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="公告不存在")

        if not _can_manage_notice_instance(request.user, instance):
            return ResponseError(msg="无权删除该类型公告")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class NoticeDetailView(APIView):
    """
    公告详情
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        if not _can_access_notice(request.user):
            return ResponseError(msg="无权查看公告")

        instance = Notice.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="公告不存在")

        if instance.notice_type not in _notice_type_scope(request.user):
            return ResponseError(msg="无权查看该类型公告")

        if not _can_publish_notice(request.user) and instance.status != "published":
            return ResponseError(msg="无权查看草稿公告")

        serializer = NoticeSerializer(instance)

        return ResponseSuccess(data=serializer.data)
