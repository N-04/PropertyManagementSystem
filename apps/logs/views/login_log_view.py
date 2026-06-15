# 文件说明：处理 apps/logs/views/login_log_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView

from common.response.response import ResponseSuccess
from apps.logs.models.login_log import LoginLog
from apps.logs.serializers.login_log_serializer import LoginLogSerializer
from apps.users.models import user


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

    def get(self, request):

        queryset = LoginLog.objects.all().order_by("-id")

        serializer = LoginLogSerializer(
            queryset,
            many=True,
        )

        return ResponseSuccess(data=serializer.data)
