# 文件说明：处理 apps/repairs/views/repair_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.logs.services.log_service import save_operation_log
from apps.owners.models import Owner
from apps.repairs.models import Repair, RepairLog
from apps.repairs.serializers.repair_serializer import RepairSerializer
from apps.users.models import User
from apps.users.utils.role_access import has_any_role, is_owner_user, is_repair_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import (
    ResponseError,
    ResponseSuccess,
)

REPAIR_MANAGE_ROLES = (
    "admin",
    "super_admin",
    "property_admin",
    "customer_service",
    "service",
)


# 报修权限分块：业主、维修员和物业/客服的可见范围不同。
def _can_manage_repair(user):
    """物业管理员和客服类角色可以派单、查看和维护报修工单。"""

    return has_any_role(user, *REPAIR_MANAGE_ROLES) or getattr(user, "is_superuser", False)


class RepairCreateView(APIView):
    """
    创建报修
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        if is_owner_user(request.user):
            # 业主提交报修时，房屋必须属于当前账号绑定的业主资料。
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

        # 列表按角色裁剪：业主看自己的，维修员看已分配或可接单池，管理员看全部。
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

            # 搜索只覆盖标题和报修业主，和前端“标题/业主”提示保持一致。
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(owner__name__icontains=keyword)
            )

        if status:

            queryset = queryset.filter(status=status)

        if start_time:
            queryset = queryset.filter(created_at__date__gte=start_time)

        if end_time:
            queryset = queryset.filter(created_at__date__lte=end_time)

        page_queryset, page_meta = paginate_queryset(queryset, request)
        serializer = RepairSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


# 工单状态流分块：接单、维修中、完成和评价都在更新接口内统一校验。
class RepairUpdateView(APIView):
    """修改报修，统一处理业主编辑、维修员接单流转和业主评价。"""

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

        # 维修员接无人认领工单时自动绑定自己；非认领场景只能操作已分配给自己的工单。
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
                # 评分只允许已完成工单，且每个工单只能评价一次。
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

            # 维修员状态机：接单 -> 维修中 -> 完成，禁止跳过中间状态。
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
            # 完成工单必须带维修结果，避免右侧抽屉空提交。
            return ResponseError(msg="请填写维修结果")

        # 前面已按角色收窄可写字段，这里再交给序列化器做模型级校验。
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

        saved = serializer.save()

        if is_repair_claim and not saved.repair_user.filter(id=request.user.id).exists():
            # 无人认领工单被接单后，把当前维修员写入维修人员关系。
            saved.repair_user.add(request.user)

        if mark_finished:
            saved.finish_time = timezone.now()
            saved.save(update_fields=["finish_time"])

        action = "修改报修"

        # 操作日志动作按业务事件归类，方便管理员审计工单流转。
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

        # 删除权限跟查看权限保持一致：业主只删自己的，管理员才能处理全部。
        if is_owner_user(request.user):
            if instance.owner.phone != request.user.phone:
                return ResponseError(msg="无权删除该报修")
        elif not _can_manage_repair(request.user):
            return ResponseError(msg="无权删除该报修")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class RepairDetailView(APIView):
    """报修详情，按当前角色校验可见范围。"""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
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

        # 维修员可以查看待接单池；已有人接单后只能由对应维修员查看。
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

        serializer = RepairSerializer(instance)

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

        # 重新派单前先清空旧人员，避免同一工单残留多个无效维修员。
        repair.repair_user.clear()

        users = User.objects.filter(id__in=repair_users)

        if not users.exists():
            return ResponseError(msg="维修人员不存在")

        repair.repair_user.add(*users)

        # 派单后进入待接单状态，维修员随后在工作台接单。
        repair.status = "assigned"

        repair.save()

        RepairLog.objects.create(
            repair=repair,
            operator=request.user,
            action="分配维修人员",
        )

        return ResponseSuccess(msg="分配成功")
