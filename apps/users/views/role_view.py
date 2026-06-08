from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from common.response.response import ResponseSuccess, ResponseError
from rest_framework.views import APIView

from apps.users.models.role import Role
from apps.users.serializers.role_serializer import RoleSerializer


# =====================================================
# 新增角色
# =====================================================
class RoleCreateView(APIView):

    def post(self, request):

        # 获取角色名称
        name = request.data.get("name")

        # 获取角色编码
        code = request.data.get("code")

        # =====================================================
        # 数据校验
        # =====================================================

        # 角色名称不能为空
        if not name:

            return Response({"code": 400, "msg": "角色名称不能为空"})

        # 角色编码不能为空
        if not code:

            return Response({"code": 400, "msg": "角色编码不能为空"})

        # =====================================================
        # 判断角色编码是否存在
        # =====================================================

        if Role.objects.filter(code=code).exists():

            return Response({"code": 400, "msg": "角色编码已存在"})

        # =====================================================
        # 创建角色
        # =====================================================

        Role.objects.create(
            # 角色名称
            name=name,
            # 角色编码
            code=code,
        )

        # =====================================================
        # 返回结果
        # =====================================================

        return Response({"code": 200, "msg": "创建成功"})


# =====================================================
# 角色列表
# =====================================================
class RoleListView(APIView):

    def get(self, request):

        # 查询全部角色
        roles = Role.objects.all()

        # 序列化
        serializer = RoleSerializer(roles, many=True)

        # 返回结果
        return Response({"code": 200, "data": serializer.data})


class RoleDetailView(APIView):

    def get(self, request, pk):

        role = get_object_or_404(Role, id=pk)

        serializer = RoleSerializer(role)

        return Response({"code": 200, "data": serializer.data})


# 编辑角色接口
class RoleUpdateView(APIView):

    # 修改角色
    def put(self, request, pk):

        # 获取角色对象
        role = get_object_or_404(Role, id=pk)

        # 序列化器
        serializer = RoleSerializer(instance=role, data=request.data)

        # 验证
        serializer.is_valid(raise_exception=True)

        # 保存
        serializer.save()

        return Response({"code": 200, "msg": "修改成功"})


# =====================================================
# 删除角色
# =====================================================


class RoleDeleteView(APIView):

    # 删除角色
    def delete(self, request, pk):

        # 获取角色对象
        role = get_object_or_404(Role, id=pk)

        # 删除
        role.delete()

        # 返回结果
        return Response({"code": 200, "msg": "删除成功"})


class RolePermissionAssignView(APIView):
    """
    角色分配权限
    """

    def post(self, request):

        # ==================================
        # 获取参数
        # ==================================

        role_id = request.data.get("role_id")

        permission_ids = request.data.get("permission_ids", [])

        # ==================================
        # 查询角色
        # ==================================

        role = Role.objects.filter(id=role_id).first()

        if not role:

            return ResponseError(msg="角色不存在")

        # ==================================
        # 重新绑定权限
        # ==================================

        role.permissions.set(permission_ids)

        # ==================================
        # 返回结果
        # ==================================

        return ResponseSuccess(msg="授权成功")
