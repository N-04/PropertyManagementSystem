from rest_framework.permissions import BasePermission
from apps.users.models.permission import Permission


class AuthPermission(BasePermission):

    def has_permission(self, request, view):

        # 未登录
        if not request.user or not request.user.is_authenticated:
            return False

        # 超级管理员直接放行
        if request.user.is_superuser:
            return True

        # 获取当前接口路径
        path = request.path

        # 获取请求方法
        method = request.method

        # 查询权限
        permission = Permission.objects.filter(
            path=path,
            method=method
        ).first()

        # 接口没配置权限
        if not permission:
            return True

        # 获取用户所有角色
        roles = request.user.roles.all()

        # 获取角色所有权限 code
        permission_codes = []

        for role in roles:
            permissions = role.permissions.all()

            for item in permissions:
                permission_codes.append(item.code)

        # 判断权限
        if permission.code in permission_codes:
            return True

        return False