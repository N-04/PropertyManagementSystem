from rest_framework.views import APIView

from apps.users.models.menu import Menu
from apps.users.serializers.menu_serializer import MenuSerializer
from common.response.response import ResponseError, ResponseSuccess
from rest_framework.response import Response


class MenuCreateView(APIView):

    def post(self, request):

        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():

            menu_obj = serializer.save()

            return ResponseSuccess(data=MenuSerializer(menu_obj).data, msg="创建成功")

        return ResponseError(msg="参数错误", data=serializer.errors)


class MenuListView(APIView):

    def get(self, request):

        queryset = Menu.objects.all().order_by("sort")

        serializer = MenuSerializer(queryset, many=True)

        return Response({"code": 200, "data": serializer.data})


class MenuTreeView(APIView):
    """

    菜单树接口

    功能：

    用户登录后，根据用户拥有的角色和权限，

    动态返回当前用户可访问的菜单树。

    """

    def get(self, request):

        # ==================================

        # 获取当前登录用户

        # ==================================

        user = request.user

        # ==================================

        # 收集用户拥有的菜单ID

        # User

        #   ↓

        # Role

        #   ↓

        # Permission

        #   ↓

        # Menu

        # ==================================

        menu_ids = []

        # 遍历用户所有角色

        for role in user.roles.all():

            # 遍历角色拥有的权限

            for permission in role.permissions.all():

                # 如果权限绑定了菜单

                if permission.menu:

                    menu_ids.append(permission.menu.id)

        # 去重

        menu_ids = list(set(menu_ids))

        # ==================================

        # 递归生成菜单树

        # ==================================

        def build_tree(menu):
            """

            递归生成菜单树

            参数：

                menu 当前菜单对象

            返回：

                dict

            """

            # 查询当前菜单下的子菜单

            children = Menu.objects.filter(parent=menu, id__in=menu_ids).order_by(
                "sort"
            )

            return {
                "id": menu.id,
                "title": menu.title,
                "icon": menu.icon,
                "path": menu.path,
                "component": menu.component,
                # 递归加载子菜单
                "children": [build_tree(child) for child in children],
            }

        # ==================================

        # 查询一级菜单

        # ==================================

        roots = Menu.objects.filter(parent__isnull=True, id__in=menu_ids).order_by(
            "sort"
        )

        # ==================================

        # 构建完整菜单树

        # ==================================

        data = [build_tree(menu) for menu in roots]

        # ==================================

        # 返回结果

        # ==================================

        return ResponseSuccess(data=data)


class UserMenuTreeView(APIView):
    """
    当前登录用户菜单树
    """

    def get(self, request):
        """
        获取当前用户菜单树
        """

        # 当前用户
        user = request.user

        # 菜单ID集合
        menu_ids = []

        # 遍历用户角色
        for role in user.roles.all():

            # 遍历角色权限
            for permission in role.permissions.all():

                if permission.menu:
                    menu_ids.append(permission.menu.id)

        # 去重
        menu_ids = list(set(menu_ids))

        # 一级菜单
        root_menus = Menu.objects.filter(
            parent__isnull=True,
            id__in=menu_ids,
        ).order_by("sort")

        def build_tree(menu):
            """
            递归菜单树
            """

            children = Menu.objects.filter(
                parent=menu,
                id__in=menu_ids,
            ).order_by("sort")

            return {
                "id": menu.id,
                "title": menu.title,
                "icon": menu.icon,
                "path": menu.path,
                "component": menu.component,
                "children": [build_tree(child) for child in children],
            }

        data = [build_tree(menu) for menu in root_menus]

        return ResponseSuccess(data=data)
