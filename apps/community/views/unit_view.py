# 文件说明：处理 apps/community/views/unit_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.community.models import Unit
from apps.community.serializers.unit_serializer import UnitSerializer

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)


class UnitCreateView(APIView):
    """
    创建单元
    """

    def post(self, request):

        serializer = UnitSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return ResponseSuccess(
                data=serializer.data,
                msg="创建成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class UnitListView(APIView):
    """
    单元列表
    """

    def get(self, request):

        queryset = Unit.objects.all().order_by("-id")

        serializer = UnitSerializer(
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
