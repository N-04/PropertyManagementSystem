# 文件说明：处理 common/views/base_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BaseView(APIView):
    """统一给继承视图加登录认证，具体业务权限仍由子类自行收窄。"""

    permission_classes = [IsAuthenticated]
