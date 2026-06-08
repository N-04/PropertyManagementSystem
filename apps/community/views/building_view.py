from rest_framework.views import APIView

from apps.community.models import Building
from apps.community.serializers.building_serializer import BuildingSerializer
from rest_framework.response import Response
from common.response.response import ResponseSuccess, ResponseError


class BuildingCreateView(APIView):
    """
    创建楼栋
    """

    def post(self, request):

        serializer = BuildingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return ResponseSuccess(data=serializer.data, msg="创建成功")

        return ResponseError(msg="参数错误", data=serializer.errors)


class BuildingListView(APIView):
    """

    楼栋列表

    """

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
