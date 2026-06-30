# 文件说明：处理 apps/users/views/menu_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models.menu import Menu
from apps.users.serializers.menu_serializer import MenuSerializer
from apps.users.utils.role_access import has_any_role
from common.response.response import ResponseError, ResponseSuccess
from rest_framework.response import Response


RBAC_MANAGE_ROLES = ("admin", "super_admin", "property_admin")
DEPRECATED_USER_MENU_TITLES = {
    "联系客服",
    "派单处理",
    "派单管理",
    "停车缴费",
    "车位缴费",
    "停车费缴纳",
    "车位费缴纳",
}
DEPRECATED_USER_MENU_PATHS = {
    "/contact/service",
}


def _can_manage_rbac(user):
    """RBAC 菜单管理只允许管理员角色访问，避免普通角色绕过前端直接调用。"""

    return has_any_role(user, *RBAC_MANAGE_ROLES) or getattr(user, "is_superuser", False)


def _rbac_forbidden_response():
    return ResponseError(msg="无权访问权限管理", code=403)


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


def _is_deprecated_user_menu(menu):
    """过滤旧数据库残留菜单，保持后端菜单和当前前端交互口径一致。"""

    title = (menu.title or "").strip()
    path = (menu.path or "").strip()

    return title in DEPRECATED_USER_MENU_TITLES or path in DEPRECATED_USER_MENU_PATHS


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
    """递归构建当前用户可见的菜单节点。"""

    if _is_deprecated_user_menu(menu):
        return None

    children = Menu.objects.filter(
        parent=menu,
        id__in=menu_ids,
        hidden=False,
    ).order_by("sort", "id")

    child_nodes = []

    for child in children:
        # 子节点可能是旧菜单或隐藏菜单，递归返回空时不加入最终菜单树。
        child_node = _build_menu_tree(child, menu_ids)

        if child_node:
            child_nodes.append(child_node)

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
        "children": child_nodes,
    }


def _build_menu_tree_list(menus, menu_ids):
    """把根菜单集合转成前端可直接渲染的树形列表。"""

    data = []

    for menu in menus:
        menu_node = _build_menu_tree(menu, menu_ids)

        if menu_node:
            data.append(menu_node)

    return data


class MenuCreateView(APIView):
    """后台菜单创建接口，仅管理员角色可用。"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():

            menu_obj = serializer.save()

            return ResponseSuccess(data=MenuSerializer(menu_obj).data, msg="创建成功")

        return ResponseError(msg="参数错误", data=serializer.errors)


class MenuListView(APIView):
    """后台菜单平铺列表，用于角色配置和菜单维护。"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _can_manage_rbac(request.user):
            return _rbac_forbidden_response()

        queryset = Menu.objects.all().order_by("sort", "id")

        serializer = MenuSerializer(queryset, many=True)

        return Response({"code": 200, "data": serializer.data})


class MenuTreeView(APIView):
    """
    菜单树接口

    用户登录后，根据用户拥有的角色和权限动态返回当前用户可访问的菜单树。
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 权限菜单分块：先收集用户权限，再只查询根菜单，子级交给递归函数处理。
        user = request.user
        menu_ids = _get_user_menu_ids(user)

        roots = Menu.objects.filter(
            parent__isnull=True,
            id__in=menu_ids,
            hidden=False,
        ).order_by(
            "sort",
            "id",
        )

        data = _build_menu_tree_list(roots, menu_ids)

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

        # 和 MenuTreeView 保持相同口径，给前端布局层提供当前用户菜单。
        user = request.user
        menu_ids = _get_user_menu_ids(user)

        root_menus = Menu.objects.filter(
            parent__isnull=True,
            id__in=menu_ids,
            hidden=False,
        ).order_by("sort", "id")

        data = _build_menu_tree_list(root_menus, menu_ids)

        return ResponseSuccess(data=data)
