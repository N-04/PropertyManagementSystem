# 文件说明：处理 apps/logs/views/login_log_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from common.response.response import ResponseSuccess, ResponseError
from apps.logs.models.login_log import LoginLog
from apps.logs.serializers.login_log_serializer import LoginLogSerializer
from apps.users.models import user
from apps.users.utils.role_access import is_property_manager_user


class LoginView(APIView):

    def post(self, request):

        ...

        LoginLog.objects.create(
            username=user.username,
            ip=request.META.get("REMOTE_ADDR"),
        )

        return ResponseSuccess(...)


class LoginLogListView(APIView):
    """

    登录日志列表

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权查看登录日志")

        queryset = LoginLog.objects.all().order_by("-id")

        serializer = LoginLogSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)
