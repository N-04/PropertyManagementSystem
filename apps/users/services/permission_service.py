# 文件说明：封装 apps/users/services/permission_service.py 对应业务的可复用服务逻辑。

from django.db.models import Q

from apps.users.models.permission import Permission


class PermissionService:
    """权限管理服务，封装权限列表查询与基础增删改操作。"""

    @staticmethod
    def get_permission_list(params):
        """按关键字筛选权限标题或权限编码。"""

        queryset = Permission.objects.all().order_by('-id')

        keyword = params.get('keyword')

        if keyword:
            # 权限列表支持同时搜索中文名称和接口/菜单权限编码。
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(code__icontains=keyword)
            )

        return queryset

    @staticmethod
    def get_permission_by_id(pk):
        """查询单个权限；不存在时返回 None 交给视图层生成响应。"""

        try:
            return Permission.objects.get(pk=pk)

        except Permission.DoesNotExist:
            return None

    @staticmethod
    def create_permission(serializer):
        """通过已校验的 serializer 创建权限。"""

        permission_obj = serializer.save()

        return permission_obj

    @staticmethod
    def update_permission(serializer):
        """通过已校验的 serializer 更新权限。"""

        permission_obj = serializer.save()

        return permission_obj

    @staticmethod
    def delete_permission(permission_obj):
        """删除权限对象，调用方负责确认权限存在和可删除。"""
        permission_obj.delete()
