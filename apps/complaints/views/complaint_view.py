# 文件说明：处理投诉建议列表、提交、处理和回访接口。
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.complaints.models import Complaint
from apps.complaints.serializers import ComplaintSerializer
from apps.owners.models import Owner
from apps.users.utils.role_access import is_owner_user
from common.response.response import ResponseError, ResponseSuccess


def _owner_filter(user):
    return Q(owner__phone=user.phone) | Q(phone=user.phone)


def _can_owner_access(user, complaint):
    return complaint.phone == user.phone or (
        complaint.owner and complaint.owner.phone == user.phone
    )


def _base_queryset(request):
    queryset = Complaint.objects.select_related("owner", "handler").all()

    if is_owner_user(request.user):
        queryset = queryset.filter(_owner_filter(request.user))

    return queryset


class ComplaintListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = _base_queryset(request)
        keyword = request.GET.get("keyword")
        category = request.GET.get("category")
        status = request.GET.get("status")

        if keyword:
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

        serializer = ComplaintSerializer(queryset, many=True)
        return ResponseSuccess(data=serializer.data)


class ComplaintCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        if is_owner_user(request.user):
            owner = Owner.objects.filter(phone=request.user.phone).first()

            if owner:
                data["owner"] = owner.id

            data["phone"] = data.get("phone") or request.user.phone

        serializer = ComplaintSerializer(data=data)

        if not serializer.is_valid():
            return ResponseError(msg="参数错误", data=serializer.errors)

        complaint = serializer.save()
        return ResponseSuccess(data=ComplaintSerializer(complaint).data, msg="提交成功")


class ComplaintDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)

        if is_owner_user(request.user) and not _can_owner_access(request.user, complaint):
            return ResponseError(msg="无权查看该投诉")

        return ResponseSuccess(data=ComplaintSerializer(complaint).data)


class ComplaintUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)

        if is_owner_user(request.user):
            if not _can_owner_access(request.user, complaint):
                return ResponseError(msg="无权操作该投诉")

            if complaint.status != "pending":
                return ResponseError(msg="已受理的投诉不能修改")

            allowed_fields = {"title", "content", "category", "phone"}
            data = {key: request.data[key] for key in allowed_fields if key in request.data}
        else:
            data = request.data.copy()

        serializer = ComplaintSerializer(complaint, data=data, partial=True)

        if not serializer.is_valid():
            return ResponseError(msg="参数错误", data=serializer.errors)

        saved = serializer.save(handler=request.user if not is_owner_user(request.user) else complaint.handler)
        return ResponseSuccess(data=ComplaintSerializer(saved).data, msg="处理成功")


class ComplaintDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)

        if is_owner_user(request.user):
            if not _can_owner_access(request.user, complaint):
                return ResponseError(msg="无权删除该投诉")

            if complaint.status != "pending":
                return ResponseError(msg="已受理的投诉不能删除")

        complaint.delete()
        return ResponseSuccess(msg="删除成功")
