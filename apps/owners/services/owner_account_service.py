# 文件说明：维护业主资料与系统登录账号之间的对应关系。

import re
import string
from secrets import choice

from django.contrib.auth import get_user_model

from apps.owners.models import Owner
from apps.users.models.role import Role

PASSWORD_SPECIAL_CHARS = "@#$%&*?"


def _username_from_owner(owner: Owner) -> str:
    """根据业主手机号生成稳定用户名，并清理用户名不支持的字符。"""

    phone = (owner.phone or "").strip()
    clean_phone = re.sub(r"[^0-9A-Za-z_@.+-]", "_", phone)
    return f"owner_{clean_phone or owner.id}"


def _unique_username(base_username: str) -> str:
    """生成不与已有用户冲突的用户名。"""

    User = get_user_model()

    if not User.objects.filter(username=base_username).exists():
        return base_username

    index = 2

    while User.objects.filter(username=f"{base_username}_{index}").exists():
        index += 1

    return f"{base_username}_{index}"


def _generate_owner_initial_password(length=16) -> str:
    """生成一次性强密码，避免所有业主账号共用固定初始密码。"""

    alphabet = string.ascii_letters + string.digits + PASSWORD_SPECIAL_CHARS
    required_chars = [
        choice(string.ascii_lowercase),
        choice(string.ascii_uppercase),
        choice(string.digits),
        choice(PASSWORD_SPECIAL_CHARS),
    ]
    remaining_chars = [choice(alphabet) for _ in range(max(length - len(required_chars), 0))]
    password_chars = required_chars + remaining_chars

    # 用 secrets.choice 简单洗牌，避免固定字符类型顺序暴露密码结构。
    return "".join(password_chars.pop(choice(range(len(password_chars)))) for _ in range(len(password_chars)))


def ensure_owner_login_user(owner: Owner):
    """
    确保业主资料有对应的 owner 登录账号。

    已有账号只补齐 owner 角色和基础资料，不会重置密码；没有账号时创建一个
    可登录账号，初始密码每次随机生成，后续由管理员重置或通知业主。
    """

    phone = (owner.phone or "").strip()

    if not phone:
        return None, False

    User = get_user_model()
    owner_role, _ = Role.objects.get_or_create(
        code="owner",
        defaults={"name": "业主"},
    )
    owner_role.name = "业主"
    owner_role.save(update_fields=["name"])

    # 先复用同手机号的已注册账号，即使账号仍在待审核状态。
    # 这样“注册 -> 房产认证/创建业主资料 -> 成为正式业主”不会拆成两个登录账号。
    user = User.objects.filter(phone=phone).order_by("id").first()

    created = False

    if not user:
        user = User(
            username=_unique_username(_username_from_owner(owner)),
            phone=phone,
            real_name=owner.name,
            is_active=True,
            status=1,
            role=owner_role,
        )
        user.set_password(_generate_owner_initial_password())
        user.save()
        created = True

    update_fields = []

    if not user.real_name and owner.name:
        user.real_name = owner.name
        update_fields.append("real_name")

    if user.role_id is None:
        user.role = owner_role
        update_fields.append("role")

    if user.status != 1:
        user.status = 1
        update_fields.append("status")

    if not user.is_active:
        user.is_active = True
        update_fields.append("is_active")

    if update_fields:
        user.save(update_fields=update_fields)

    if not user.roles.filter(code="owner").exists():
        user.roles.add(owner_role)

    return user, created
