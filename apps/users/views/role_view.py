# 文件说明：处理 apps/users/views/role_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.response.response import ResponseSuccess, ResponseError
from rest_framework.views import APIView

from apps.users.models.permission import Permission
from apps.users.models.role import Role
from apps.users.serializers.role_serializer import RoleSerializer
from apps.users.utils.role_access import has_any_role


RBAC_MANAGE_ROLES = ("admin", "super_admin", "property_admin")


def _can_manage_rbac(user):
    """角色和权限分配只允许管理员角色操作。"""

    return has_any_role(user, *RBAC_MANAGE_ROLES) or getattr(user, "is_superuser", False)


def _rbac_forbidden_response():
    return ResponseError(msg="无权访问权限管理", code=403)


# =====================================================
# 新增角色
# =====================================================
class RoleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

        # 查询全部角色
        roles = Role.objects.all()

        # 序列化
        serializer = RoleSerializer(roles, many=True)

        # 返回结果
        return Response({"code": 200, "data": serializer.data})


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

        role = get_object_or_404(Role, id=pk)

        serializer = RoleSerializer(role)

        return Response({"code": 200, "data": serializer.data})


# 编辑角色接口
class RoleUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    # 修改角色
    def put(self, request, pk):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

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
    permission_classes = [IsAuthenticated]

    # 删除角色
    def delete(self, request, pk):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

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

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

        # ==================================
        # 获取参数
        # ==================================

        role_id = request.data.get("role_id")

        permission_ids = request.data.get("permission_ids", [])

        if not isinstance(permission_ids, list):
            return ResponseError(msg="permission_ids 必须是数组")

        # ==================================
        # 查询角色
        # ==================================

        role = Role.objects.filter(id=role_id).first()

        if not role:

            return ResponseError(msg="角色不存在")

        # ==================================
        # 重新绑定权限
        # ==================================

        try:
            permission_ids = [int(item) for item in permission_ids]
        except (TypeError, ValueError):
            return ResponseError(msg="权限ID必须是数字")

        permissions = Permission.objects.filter(id__in=permission_ids)
        existing_ids = set(permissions.values_list("id", flat=True))
        invalid_ids = sorted(set(permission_ids) - existing_ids)

        if invalid_ids:
            return ResponseError(msg=f"权限不存在：{invalid_ids}")

        role.permissions.set(permissions)

        # ==================================
        # 返回结果
        # ==================================

        return ResponseSuccess(
            data={
                "role_id": role.id,
                "permission_ids": sorted(existing_ids),
            },
            msg="授权成功",
        )

    def put(self, request):
        # 前端保存角色时可用 PUT 或 POST，统一复用同一套授权逻辑。
        return self.post(request)
