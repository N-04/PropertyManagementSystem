# 文件说明：封装 apps/users/services/role_service.py 对应业务的可复用服务逻辑。

from apps.users.models.role import Role


class RoleService:

    @staticmethod
    def create_role(serializer):
        return serializer.save()

    @staticmethod
    def get_role_by_id(pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None

    @staticmethod
    def get_role_list():
        return Role.objects.all().order_by('-id')