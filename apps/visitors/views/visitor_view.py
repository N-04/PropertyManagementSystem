# 文件说明：处理 apps/visitors/views/visitor_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView

from apps.visitors.models.visitor import Visitor
from common.response.response import ResponseSuccess, ResponseError
from apps.visitors.serializers.visitor_serializer import VisitorSerializer
from apps.logs.services.log_service import save_operation_log


class VisitorCreateView(APIView):
    """
    创建访客
    """

    def post(self, request):

        serializer = VisitorSerializer(data=request.data)

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

    def get(self, request):

        try:
            page = max(int(request.GET.get("page", 1)), 1)
            page_size = min(max(int(request.GET.get("page_size", 1000)), 1), 1000)
        except (TypeError, ValueError):
            return ResponseError(msg="分页参数错误")

        keyword = (request.GET.get("keyword") or "").strip()
        queryset = Visitor.objects.select_related("owner", "approve_user").all().order_by("-id")

        if keyword:
            # 支持访客、手机号、被访业主和来访事由搜索，供前端列表筛选使用。
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(phone__icontains=keyword)
                | Q(owner__name__icontains=keyword)
                | Q(reason__icontains=keyword)
            )

        start = (page - 1) * page_size
        end = start + page_size

        serializer = VisitorSerializer(
            queryset[start:end],
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class VisitorUpdateView(APIView):
    """
    修改访客
    """

    def put(self, request, pk):

        instance = Visitor.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="访客记录不存在")

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

    def delete(self, request, pk):

        instance = Visitor.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="访客记录不存在")

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

    def get(self, request, pk):

        try:
            visitor = Visitor.objects.get(pk=pk)
        except Visitor.DoesNotExist:
            return ResponseError(msg="访客不存在")

        serializer = VisitorSerializer(visitor)

        return ResponseSuccess(data=serializer.data)


class VisitorApproveView(APIView):
    """
    访客审批
    """

    def put(self, request, pk):
        """
        更新访客审批结果
        """

        # 查询访客
        visitor = Visitor.objects.filter(id=pk).first()

        if not visitor:
            return ResponseError(msg="访客不存在")

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

    def put(self, request, pk):

        visitor = Visitor.objects.filter(id=pk).first()

        if not visitor:
            return ResponseError(msg="访客不存在")

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

    def put(self, request, pk):

        visitor = Visitor.objects.filter(id=pk).first()

        if not visitor:
            return ResponseError(msg="访客不存在")

        if visitor.status != "entered":
            return ResponseError(msg="访客未到访")

        visitor.status = "left"

        visitor.leave_time = timezone.now()

        visitor.save(update_fields=["status", "leave_time"])

        return ResponseSuccess(data=VisitorSerializer(visitor).data, msg="登记成功")
