from rest_framework.views import APIView

from apps.notice.models import Notice
from apps.notice.serializers.notice_serializer import NoticeSerializer

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)
from common.utils.log import save_log


class NoticeCreateView(APIView):
    """
    创建公告
    """

    def post(self, request):

        serializer = NoticeSerializer(data=request.data)

        if serializer.is_valid():

            notice = serializer.save()

            save_log(
                username=notice.username,
                module=notice.module,
                action=f"新增公告 {notice.room_no}",
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

    def get(self, request):

        queryset = Notice.objects.all().order_by("-id")

        serializer = NoticeSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class NoticeUpdateView(APIView):
    """
    修改公告
    """

    def put(self, request, pk):

        instance = Notice.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="公告不存在")

        serializer = NoticeSerializer(
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


class NoticeDeleteView(APIView):
    """
    删除公告
    """

    def delete(self, request, pk):

        instance = Notice.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="公告不存在")

        instance.delete()

        return ResponseSuccess(msg="删除成功")


class NoticeDetailView(APIView):
    """
    公告详情
    """

    def get(self, request, pk):

        instance = Notice.objects.filter(id=pk).first()

        if not instance:
            return ResponseError(msg="公告不存在")

        serializer = NoticeSerializer(instance)

        return ResponseSuccess(data=serializer.data)
