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

        queryset = Visitor.objects.all().order_by("-id")

        serializer = VisitorSerializer(
            queryset,
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
        save_operation_log(
            username=request.user.username,
            module="访客管理",
            action=f"删除访客：{instance.name}",
        )

        if not instance:
            return ResponseError(msg="访客记录不存在")

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
