# 文件说明：处理 apps/users/views/menu_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models.menu import Menu
from apps.users.serializers.menu_serializer import MenuSerializer
from common.response.response import ResponseError, ResponseSuccess
from rest_framework.response import Response


def _with_parent_menu_ids(menu_ids):
    """
    补齐菜单父级链。

    角色通常只给具体页面或按钮权限，如果不把父级菜单也加入集合，
    前端菜单树会因为缺少一级菜单而显示为空。
    """

    all_ids = set(menu_ids)

    for menu in Menu.objects.filter(id__in=menu_ids).select_related("parent"):
        parent = menu.parent

        while parent:
            all_ids.add(parent.id)
            parent = parent.parent

    return list(all_ids)


def _get_user_menu_ids(user):
    """
    根据当前用户收集可访问菜单 ID。

    superadmin 不受角色权限限制，直接返回全部菜单。
    普通用户从多角色和主角色里收集权限绑定的菜单。
    """

    if user.is_superuser:
        return list(Menu.objects.values_list("id", flat=True))

    roles = list(user.roles.all())

    if user.role_id:
        roles.append(user.role)

    menu_ids = []

    for role in roles:
        for permission in role.permissions.select_related("menu").all():
            if permission.menu_id:
                menu_ids.append(permission.menu_id)

    return _with_parent_menu_ids(menu_ids)


def _build_menu_tree(menu, menu_ids):
    children = Menu.objects.filter(
        parent=menu,
        id__in=menu_ids,
        hidden=False,
    ).order_by("sort", "id")

    return {
        "id": menu.id,
        "title": menu.title,
        "icon": menu.icon,
        "path": menu.path,
        "component": menu.component,
        "sort": menu.sort,
        "hidden": menu.hidden,
        "menu_type": menu.menu_type,
        "parent_id": menu.parent_id,
        "children": [_build_menu_tree(child, menu_ids) for child in children],
    }


class MenuCreateView(APIView):

    def post(self, request):

        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():

            menu_obj = serializer.save()

            return ResponseSuccess(data=MenuSerializer(menu_obj).data, msg="创建成功")

        return ResponseError(msg="参数错误", data=serializer.errors)


class MenuListView(APIView):

    def get(self, request):

        queryset = Menu.objects.all().order_by("sort", "id")

        serializer = MenuSerializer(queryset, many=True)

        return Response({"code": 200, "data": serializer.data})


class MenuTreeView(APIView):
    """
    菜单树接口

    功能：

    用户登录后，根据用户拥有的角色和权限，

    动态返回当前用户可访问的菜单树。

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # ==================================

        # 获取当前登录用户

        # ==================================

        user = request.user
        menu_ids = _get_user_menu_ids(user)

        # ==================================

        # 查询一级菜单

        # ==================================

        roots = Menu.objects.filter(
            parent__isnull=True,
            id__in=menu_ids,
            hidden=False,
        ).order_by(
            "sort",
            "id",
        )

        # ==================================

        # 构建完整菜单树

        # ==================================

        data = [_build_menu_tree(menu, menu_ids) for menu in roots]

        # ==================================

        # 返回结果

        # ==================================

        return ResponseSuccess(data=data)


class UserMenuTreeView(APIView):
    """
    当前登录用户菜单树
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        获取当前用户菜单树
        """

        user = request.user
        menu_ids = _get_user_menu_ids(user)

        # 一级菜单
        root_menus = Menu.objects.filter(
            parent__isnull=True,
            id__in=menu_ids,
            hidden=False,
        ).order_by("sort", "id")

        data = [_build_menu_tree(menu, menu_ids) for menu in root_menus]

        return ResponseSuccess(data=data)
