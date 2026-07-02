# 文件说明：声明 Python 包，便于模块被项目导入。

from .menu import Menu
from .permission import Permission
from .role import Role
from .user import User

__all__ = ["Menu", "Permission", "Role", "User"]
