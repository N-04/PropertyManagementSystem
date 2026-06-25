# 文件说明：处理 apps/community/views/building_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.community.models import Building
from apps.community.serializers.building_serializer import BuildingSerializer
from apps.users.utils.role_access import is_property_manager_user
from rest_framework.response import Response
from common.response.response import ResponseSuccess, ResponseError


class BuildingCreateView(APIView):
    """
    创建楼栋
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权创建楼栋")

        serializer = BuildingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return ResponseSuccess(data=serializer.data, msg="创建成功")

        return ResponseError(msg="参数错误", data=serializer.errors)


class BuildingListView(APIView):
    """

    楼栋列表

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = Building.objects.all().order_by("-id")

        serializer = BuildingSerializer(
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
