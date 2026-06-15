# 文件说明：处理 apps/users/views/permission_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

# =====================================================
# 导入 DRF APIView
# =====================================================

from rest_framework.views import APIView

# =====================================================
# 导入响应
# =====================================================

from rest_framework.response import Response

# =====================================================
# 导入权限模型
# =====================================================

from apps.users.models.permission import Permission

# =====================================================
# 导入序列化器
# =====================================================

from apps.users.serializers.permission_serializer import PermissionSerializer
from common.response.response import ResponseSuccess

# =====================================================
# 权限列表
# =====================================================


class PermissionListView(APIView):

    def get(self, request):

        # 查询全部权限
        queryset = Permission.objects.all()

        # 序列化
        serializer = PermissionSerializer(queryset, many=True)

        # 返回结果
        return Response({"code": 200, "data": serializer.data})


# =====================================================
# 权限新增
# =====================================================


class PermissionCreateView(APIView):

    def post(self, request):

        # 获取请求数据
        serializer = PermissionSerializer(data=request.data)

        # 验证数据
        if serializer.is_valid():

            # 保存
            serializer.save()

            # 返回成功
            return Response({"code": 200, "msg": "新增成功"})

        # 返回错误
        return Response({"code": 400, "msg": serializer.errors})


class PermissionTreeView(APIView):
    """
    权限树接口
    """

    def get(self, request):

        queryset = (
            Permission.objects.select_related("menu")
            .all()
            .order_by("menu__sort", "name")
        )

        data = []

        for item in queryset:

            data.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "code": item.code,
                    "menu_id": item.menu_id,
                    "menu": item.menu.title if item.menu else "",
                }
            )

        return ResponseSuccess(data=data)
