# 文件说明：处理 apps/repairs/views/repair_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.utils import timezone
from apps.repairs.serializers.repair_serializer import RepairSerializer

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from apps.logs.services.log_service import save_operation_log
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.repairs.models import Repair, RepairLog

from apps.users.models import User
from apps.owners.models import Owner
from apps.users.utils.role_access import has_any_role, is_owner_user, is_repair_user
from rest_framework.pagination import PageNumberPagination

REPAIR_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
    "customer_service",
    "service",
)


def _can_manage_repair(user):
    return has_any_role(user, *REPAIR_MANAGE_ROLES) or getattr(user, "is_superuser", False)


class RepairCreateView(APIView):
    """
    创建报修
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        if is_owner_user(request.user):
            owner = Owner.objects.filter(phone=request.user.phone).first()

            if not owner:
                return ResponseError(msg="当前账号未绑定业主信息")

            data["owner"] = owner.id
            data["house"] = data.get("house") or owner.house_id

            try:
                house_id = int(data["house"])
            except (TypeError, ValueError):
                return ResponseError(msg="房屋信息不正确")

            if house_id not in Owner.objects.filter(
                phone=request.user.phone
            ).values_list("house_id", flat=True):
                return ResponseError(msg="无权为该房屋提交报修")
        elif not _can_manage_repair(request.user):
            return ResponseError(msg="无权提交报修")

        serializer = RepairSerializer(data=data)

        if serializer.is_valid():

            serializer.save()

            save_operation_log(
                username=request.user.username,
                module="报修管理",
                action="新增报修",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class RepairListView(APIView):
    """
    报修列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = Repair.objects.all().order_by("-id")

        if is_owner_user(request.user):
            queryset = queryset.filter(owner__phone=request.user.phone)
        elif is_repair_user(request.user):
            # 维修员既能查看已分配给自己的工单，也能看到尚未绑定人员的待接单池。
            queryset = queryset.filter(
                Q(repair_user=request.user)
                | Q(status__in=["pending", "assigned"], repair_user__isnull=True)
            ).distinct()
        elif not _can_manage_repair(request.user):
            queryset = queryset.none()

        keyword = request.GET.get("keyword")

        status = request.GET.get("status")

        start_time = request.GET.get("start_time")

        end_time = request.GET.get("end_time")

        if keyword:

            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(owner__name__icontains=keyword)
            )

        if status:

            queryset = queryset.filter(status=status)

        if start_time:
            queryset = queryset.filter(created_at__date__gte=start_time)

        if end_time:
            queryset = queryset.filter(created_at__date__lte=end_time)

        serializer = RepairSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class MyPage(PageNumberPagination):
    page_size = 10


class RepairUpdateView(APIView):
    """

    修改报修

    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        # 查询报修记录

        instance = Repair.objects.filter(id=pk).first()

        if not instance:

            return ResponseError(msg="报修记录不存在")

        data = request.data.copy()

        if not (
            is_owner_user(request.user)
            or is_repair_user(request.user)
            or _can_manage_repair(request.user)
        ):
            return ResponseError(msg="无权操作该报修")

        if is_owner_user(request.user) and instance.owner.phone != request.user.phone:
            return ResponseError(msg="无权操作该报修")

        is_repair_claim = (
            is_repair_user(request.user)
            and instance.status in {"pending", "assigned"}
            and data.get("status") == "accepted"
            and not instance.repair_user.exists()
        )

        if (
            is_repair_user(request.user)
            and not is_repair_claim
            and not instance.repair_user.filter(id=request.user.id).exists()
        ):
            return ResponseError(msg="无权操作该报修")

        if is_owner_user(request.user):
            evaluation_fields = {"evaluation_score", "evaluation_content"}
            is_evaluation = any(field in data for field in evaluation_fields)

            if is_evaluation:
                if instance.status != "finished":
                    return ResponseError(msg="只能评价已完成工单")

                if instance.evaluation_score is not None or instance.evaluation_time:
                    return ResponseError(msg="该工单已评价，不能重复提交")

                data = {
                    key: data[key]
                    for key in evaluation_fields
                    if key in data
                }

                try:
                    score = Decimal(str(data.get("evaluation_score", "0")))
                except (InvalidOperation, TypeError, ValueError):
                    return ResponseError(msg="评分必须为0.5-5分")

                if score < Decimal("0.5") or score > Decimal("5"):
                    return ResponseError(msg="评分必须为0.5-5分")

                if score % Decimal("0.5") != 0:
                    return ResponseError(msg="评分必须按0.5分递增")

                data["evaluation_score"] = score
                data["evaluation_time"] = timezone.now()
            elif instance.status != "pending":
                return ResponseError(msg="已受理的报修不能编辑")
            else:
                allowed_fields = {"title", "content", "repair_images"}
                data = {key: data[key] for key in allowed_fields if key in data}
        elif is_repair_user(request.user):
            allowed_fields = {"status", "repair_result", "result_images"}
            data = {key: data[key] for key in allowed_fields if key in data}

            status_flow = {
                "pending": {"accepted"},
                "assigned": {"accepted"},
                "accepted": {"processing"},
                "processing": {"finished"},
            }
            next_status = data.get("status")

            if next_status:
                allowed_statuses = status_flow.get(instance.status, set())

                if next_status not in allowed_statuses:
                    return ResponseError(msg="当前工单状态不允许该操作")

            if data.get("repair_result") or data.get("result_images"):
                if next_status != "finished" and instance.status != "processing":
                    return ResponseError(msg="只有维修中工单可以上传维修结果")
        else:
            if instance.status != "pending" and data.get("status") != "finished":
                return ResponseError(msg="当前状态不可编辑")

        mark_finished = data.get("status") == "finished"

        if mark_finished and not (
            data.get("repair_result") or instance.repair_result or data.get("result_images")
        ):
            return ResponseError(msg="请填写维修结果")

        # 序列化校验
        serializer = RepairSerializer(
            instance=instance,
            data=data,
            partial=True,
        )

        if not serializer.is_valid():

            return ResponseError(
                msg="参数错误",
                data=serializer.errors,
            )

        # 保存

        saved = serializer.save()

        if is_repair_claim and not saved.repair_user.filter(id=request.user.id).exists():
            saved.repair_user.add(request.user)

        if mark_finished:
            saved.finish_time = timezone.now()
            saved.save(update_fields=["finish_time"])

        action = "修改报修"

        if data.get("status") == "accepted":
            action = "维修员接单"
        elif data.get("status") == "processing":
            action = "开始维修"
        elif request.data.get("repair_result") or request.data.get("result_images"):
            action = "上传维修结果"
        elif data.get("evaluation_score"):
            action = f"维修评价（{data.get('evaluation_score')}分）"

        if action != "修改报修":
            RepairLog.objects.create(
                repair=instance,
                operator=request.user,
                action=action,
            )

        # 操作日志

        save_operation_log(
            username=request.user.username,
            module="报修管理",
            action=f"{action}：{instance.title}",
        )

        return ResponseSuccess(
            data=RepairSerializer(saved).data,
            msg="评价提交成功，已反馈维修人员和管理员" if data.get("evaluation_score") else "修改成功",
        )


class RepairDeleteView(APIView):
    """
    删除报修
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        instance = Repair.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="报修记录不存在")

        if is_owner_user(request.user):
            if instance.owner.phone != request.user.phone:
                return ResponseError(msg="无权删除该报修")
        elif not _can_manage_repair(request.user):
            return ResponseError(msg="无权删除该报修")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class RepairDetailView(APIView):
    """

    报修详情

    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # 查询报修记录

        instance = get_object_or_404(
            Repair,
            pk=pk,
        )

        if is_owner_user(request.user) and instance.owner.phone != request.user.phone:
            return ResponseError(msg="无权查看该报修")

        is_unclaimed_repair = (
            instance.status in {"pending", "assigned"}
            and not instance.repair_user.exists()
        )

        if (
            is_repair_user(request.user)
            and not is_unclaimed_repair
            and not instance.repair_user.filter(id=request.user.id).exists()
        ):
            return ResponseError(msg="无权查看该报修")

        if not (
            is_owner_user(request.user)
            or is_repair_user(request.user)
            or _can_manage_repair(request.user)
        ):
            return ResponseError(msg="无权查看该报修")

        # 序列化

        serializer = RepairSerializer(instance)

        # 返回数据

        return ResponseSuccess(
            data=serializer.data,
            msg="查询成功",
        )


class RepairAssignView(APIView):
    """
    分配维修人员
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if not _can_manage_repair(request.user):
            return ResponseError(msg="无权派单")

        repair = get_object_or_404(Repair, pk=pk)

        repair_users = request.data.get("repair_user", [])

        if repair.status not in {"pending", "assigned"}:
            return ResponseError(msg="当前工单状态不可派单")

        if not repair_users:
            return ResponseError(msg="请选择维修人员")

        # 清空旧人员

        repair.repair_user.clear()

        # 添加维修人员

        users = User.objects.filter(id__in=repair_users)

        if not users.exists():
            return ResponseError(msg="维修人员不存在")

        repair.repair_user.add(*users)

        # 修改状态

        repair.status = "assigned"

        repair.save()

        RepairLog.objects.create(
            repair=repair,
            operator=request.user,
            action="分配维修人员",
        )

        return ResponseSuccess(msg="分配成功")
