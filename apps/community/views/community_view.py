# 文件说明：处理 apps/community/views/community_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.community.models import Community
from apps.community.serializers import CommunitySerializer
from apps.users.utils.role_access import is_property_manager_user

from common.response.response import ResponseSuccess, ResponseError


class CommunityCreateView(APIView):
    """
    新增小区
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权新增小区")

        serializer = CommunitySerializer(data=request.data)

        if serializer.is_valid():

            community = serializer.save()

            return ResponseSuccess(
                data=CommunitySerializer(community).data, msg="创建成功"
            )

        return ResponseError(msg="参数错误", data=serializer.errors)


class CommunityListView(APIView):
    """
    小区列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = Community.objects.all().order_by("id")

        serializer = CommunitySerializer(queryset, many=True)

        return ResponseSuccess(data=serializer.data)
