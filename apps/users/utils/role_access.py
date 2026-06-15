# 文件说明：提供当前登录用户的角色判断工具，供业务接口做数据隔离。


def get_user_role_codes(user):
    """收集用户拥有的角色编码，兼容主角色和多角色。"""
    if not user or not getattr(user, "is_authenticated", False):
        return set()

    role_codes = set(user.roles.values_list("code", flat=True))

    if user.role_id:
        role_codes.add(user.role.code)

    if user.is_superuser:
        role_codes.add("super_admin")

    return role_codes


def has_any_role(user, *role_codes):
    return bool(get_user_role_codes(user) & set(role_codes))


def is_owner_user(user):
    return has_any_role(user, "owner")


def is_repair_user(user):
    return has_any_role(user, "repair_staff", "repairer", "repair")
