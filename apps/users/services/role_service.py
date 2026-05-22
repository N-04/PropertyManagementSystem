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