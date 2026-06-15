# 文件说明：封装接口访问权限校验逻辑。

from rest_framework.permissions import BasePermission


class AuthPermission(BasePermission):

    def has_permission(self, request, view):

        # 未登录
        if not request.user or not request.user.is_authenticated:
            return False

        # 超级管理员直接放行
        if request.user.is_superuser:
            return True

        # 获取用户所有角色
        roles = list(request.user.roles.all())

        if request.user.role_id:
            roles.append(request.user.role)

        # 获取角色所有权限 code
        permission_codes = []

        for role in roles:
            permissions = role.permissions.all()

            for item in permissions:
                permission_codes.append(item.code)

        # 当前项目暂未在权限表落接口路径字段，保留登录校验，接口权限后续再接表结构。
        return True
