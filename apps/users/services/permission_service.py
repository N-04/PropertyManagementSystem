# 文件说明：封装 apps/users/services/permission_service.py 对应业务的可复用服务逻辑。

from django.db.models import Q

from apps.users.models.permission import Permission


class PermissionService:

    @staticmethod
    def get_permission_list(params):

        queryset = Permission.objects.all().order_by('-id')

        keyword = params.get('keyword')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(code__icontains=keyword)
            )

        return queryset

    @staticmethod
    def get_permission_by_id(pk):

        try:
            return Permission.objects.get(pk=pk)

        except Permission.DoesNotExist:
            return None

    @staticmethod
    def create_permission(serializer):

        permission_obj = serializer.save()

        return permission_obj

    @staticmethod
    def update_permission(serializer):

        permission_obj = serializer.save()

        return permission_obj

    @staticmethod
    def delete_permission(permission_obj):
        permission_obj.delete()
