# 文件说明：处理 common/views/base_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class BaseView(APIView):

    permission_classes = [IsAuthenticated]