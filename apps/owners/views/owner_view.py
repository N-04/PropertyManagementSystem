from django.db.migrations import serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.logs.services.log_service import save_operation_log
from apps.owners.models import Owner
from apps.owners.serializers.owner_serializer import OwnerSerializer
from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
import re

from django.db.models import Q
from common.utils.log import save_log


class OwnerCreateView(APIView):
    """
    创建业主
    """

    def post(self, request):
        pattern = r"^\d{17}[\dXx]$"

        if not re.match(pattern, request.data.get("id_card")):
            return ResponseError(msg="身份证格式错误")

        serializer = OwnerSerializer(data=request.data)

        if serializer.is_valid():
            house = serializer.validated_data["house"]

            if serializer.validated_data.get("is_primary"):

                exists = Owner.objects.filter(
                    house=house,
                    is_primary=True,
                ).exists()

                if exists:
                    return ResponseError(msg="该房屋已有主业主")

            owner = serializer.save()

            # 记录操作日志
            save_operation_log(
                username=request.user.username,
                module="业主管理",
                action=f"新增业主：{serializer.validated_data.get('name')}",
            )

            save_log(
                username="admin2",
                module="业主管理",
                action=f"新增业主 {owner.name}",
            )

            file = serializer.save()
            save_log(
                username="admin2",
                module="文件上传",
                action=f"上传文件 {file.name}",
            )
            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class OwnerListView(APIView):
    """
    业主列表
    """

    def get(self, request):

        keyword = request.GET.get("keyword")

        queryset = Owner.objects.all()

        if keyword:

            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(phone__icontains=keyword)
            )

        queryset = Owner.objects.all().order_by("-id")

        serializer = OwnerSerializer(
            queryset,
            many=True,
        )

        return Response(
            {
                "code": 200,
                "msg": "success",
                "data": serializer.data,
            }
        )


class OwnerUpdateView(APIView):
    """
    修改业主
    """

    def put(self, request, pk):

        try:
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return ResponseError(msg="业主不存在")

        if request.data.get("id_card"):
            pattern = r"^\d{17}[\dXx]$"

            id_card = request.data.get("id_card")

            if not id_card:
                return ResponseError(msg="身份证不能为空")

            if not re.match(pattern, id_card):
                return ResponseError(msg="身份证格式错误")

        serializer = OwnerSerializer(
            owner,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            instance = Owner.objects.filter(id=pk).first()
            serializer.save()
            save_operation_log(
                username=request.user.username,
                module="业主管理",
                action=f"修改业主：{instance.name}",
            )
            save_log(
                username="admin2",
                module="业主管理",
                action=f"修改业主 {owner.name}",
            )

            if serializer.validated_data.get("is_primary"):

                house = serializer.validated_data.get(
                    "house",
                    owner.house,
                )

                exists = (
                    Owner.objects.filter(
                        house=house,
                        is_primary=True,
                    )
                    .exclude(
                        id=owner.id,
                    )
                    .exists()
                )

                if exists:
                    return ResponseError(msg="该房屋已有主业主")

            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class OwnerDeleteView(APIView):
    def delete(self, request, pk):
        instance = Owner.objects.filter(id=pk).first()

        if serializer.is_valid():
            save_log(
                username="admin2",
                module="业主管理",
                action=f"删除业主 {instance.name}",
            )

        if not instance:
            return ResponseError(msg="业主不存在")

        save_operation_log(
            username=request.user.username,
            module="业主管理",
            action=f"删除业主：{instance.name}",
        )

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class OwnerDetailView(APIView):
    """
    业主详情
    """

    def get(self, request, pk):

        try:
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return ResponseError(msg="业主不存在")

        serializer = OwnerSerializer(owner)

        return ResponseSuccess(data=serializer.data)
