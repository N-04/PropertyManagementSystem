# 文件说明：封装 apps/users/services/role_service.py 对应业务的可复用服务逻辑。

from apps.users.models.role import Role


class RoleService:
    """角色管理服务，封装角色基础查询和创建逻辑。"""

    @staticmethod
    def create_role(serializer):
        """通过已校验的 serializer 创建角色。"""
        return serializer.save()

    @staticmethod
    def get_role_by_id(pk):
        """按主键查询角色；不存在时返回 None 方便视图层统一响应。"""
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None

    @staticmethod
    def get_role_list():
        """按最新创建顺序返回角色列表。"""
        return Role.objects.all().order_by('-id')
