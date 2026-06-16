# 文件说明：按物业系统角色生成演示账号，并同步菜单、权限和角色授权。

import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.crypto import get_random_string

from apps.community.models import House
from apps.owners.models import Owner
from apps.users.models.menu import Menu
from apps.users.models.permission import Permission
from apps.users.models.role import Role


def menu_node(code, title, path=None, children=None, hidden=False):
    """构造菜单大纲节点，code 用于生成稳定权限编码。"""

    return {
        "code": code,
        "title": title,
        "path": path,
        "hidden": hidden,
        "children": children or [],
    }


MENU_TREE = [
    menu_node(
        "auth",
        "登录认证模块",
        children=[
            menu_node(
                "auth-login",
                "登录",
                children=[
                    menu_node("auth-login-phone", "手机号登录"),
                    menu_node("auth-login-password", "密码登录", "/login"),
                    menu_node("auth-login-captcha", "图形验证码"),
                    menu_node("auth-login-jwt", "JWT认证"),
                    menu_node("auth-logout", "退出登录"),
                ],
            ),
            menu_node(
                "auth-register",
                "注册",
                "/register",
                [
                    menu_node(
                        "auth-register-phone",
                        "手机号验证",
                        children=[
                            menu_node("auth-register-phone-required", "手机号不能为空"),
                            menu_node("auth-register-phone-length", "11位手机号"),
                            menu_node("auth-register-phone-one", "第一位必须为1"),
                            menu_node("auth-register-phone-range", "第二位3-9"),
                            menu_node("auth-register-phone-unique", "手机号唯一"),
                        ],
                    ),
                    menu_node(
                        "auth-register-name",
                        "真实姓名验证",
                        children=[
                            menu_node("auth-register-name-required", "必填项"),
                            menu_node("auth-register-name-length", "长度限制"),
                        ],
                    ),
                    menu_node(
                        "auth-register-id-card",
                        "身份证验证",
                        children=[
                            menu_node("auth-register-id-card-length", "18位身份证"),
                            menu_node("auth-register-id-card-format", "身份证格式校验"),
                            menu_node("auth-register-id-card-birthday", "出生日期校验"),
                            menu_node("auth-register-id-card-unique", "身份证唯一"),
                            menu_node("auth-register-id-card-mask", "身份证脱敏显示"),
                        ],
                    ),
                    menu_node(
                        "auth-register-password",
                        "密码验证",
                        children=[
                            menu_node("auth-register-password-length", "长度8-20位"),
                            menu_node("auth-register-password-number", "不能纯数字"),
                            menu_node("auth-register-password-letter", "不能纯字母"),
                            menu_node("auth-register-password-special", "支持特殊字符"),
                            menu_node("auth-register-password-confirm", "两次密码一致"),
                        ],
                    ),
                    menu_node(
                        "auth-register-captcha",
                        "图形验证码",
                        children=[
                            menu_node("auth-register-captcha-rule", "字母数字组合"),
                            menu_node("auth-register-captcha-refresh", "点击刷新"),
                            menu_node("auth-register-captcha-check", "验证码校验"),
                        ],
                    ),
                    menu_node(
                        "auth-register-sms",
                        "短信验证码",
                        children=[
                            menu_node("auth-register-sms-get", "获取验证码"),
                            menu_node("auth-register-sms-countdown", "60秒倒计时"),
                            menu_node("auth-register-sms-redis", "Redis缓存"),
                            menu_node("auth-register-sms-ttl", "5分钟有效期"),
                            menu_node("auth-register-sms-expired", "过期提醒"),
                        ],
                    ),
                    menu_node(
                        "auth-register-agreement",
                        "用户协议",
                        children=[
                            menu_node("auth-register-agreement-read", "阅读协议"),
                            menu_node("auth-register-agreement-check", "勾选协议"),
                            menu_node("auth-register-agreement-allow", "满足上面两点才允许注册"),
                        ],
                    ),
                    menu_node(
                        "auth-register-audit",
                        "注册审核流程",
                        children=[
                            menu_node("auth-register-audit-submit", "提交注册"),
                            menu_node("auth-register-audit-admin", "管理员审核"),
                            menu_node("auth-register-audit-house", "房产认证"),
                            menu_node("auth-register-audit-owner", "成为正式业主"),
                        ],
                    ),
                ],
            ),
            menu_node(
                "auth-reset-password",
                "找回密码",
                children=[
                    menu_node("auth-reset-phone", "手机号验证"),
                    menu_node("auth-reset-sms", "短信验证码"),
                    menu_node("auth-reset-password-action", "重置密码"),
                ],
            ),
        ],
    ),
    menu_node(
        "rbac",
        "RBAC权限管理模块",
        children=[
            menu_node("rbac-user", "用户管理", "/user/list"),
            menu_node("rbac-role", "角色管理", "/role/list"),
            menu_node("rbac-permission", "权限管理", "/permission/list"),
            menu_node("rbac-menu", "菜单管理", "/menu/list", hidden=True),
            menu_node("rbac-api", "接口权限", "/permission/list", hidden=True),
        ],
    ),
    menu_node(
        "admin",
        "管理员模块",
        children=[
            menu_node(
                "admin-super",
                "超级管理员",
                children=[
                    menu_node("admin-super-config", "系统配置"),
                    menu_node("admin-super-permission", "权限分配", "/role/list"),
                    menu_node("admin-super-manager", "管理员管理", "/user/list"),
                    menu_node("admin-super-backup", "数据备份"),
                    menu_node("admin-super-audit-log", "日志审计", "/log/list"),
                    menu_node("admin-super-monitor", "系统监控", "/dashboard", hidden=True),
                ],
            ),
            menu_node(
                "admin-property",
                "物业管理员",
                children=[
                    menu_node(
                        "admin-property-user",
                        "用户管理",
                        children=[
                            menu_node("admin-property-owner", "业主管理", "/owner/list"),
                            menu_node("admin-property-repairer", "维修员管理", "/user/list"),
                            menu_node("admin-property-service", "客服人员管理", "/user/list"),
                            menu_node("admin-property-finance", "财务人员管理", "/user/list"),
                            menu_node("admin-property-realname", "实名认证审核", "/user/list"),
                        ],
                    ),
                    menu_node(
                        "admin-property-community",
                        "小区管理",
                        children=[
                            menu_node("admin-property-community-info", "小区信息", "/community/list"),
                            menu_node("admin-property-building", "楼栋管理", "/building/list"),
                            menu_node("admin-property-unit", "单元管理", "/unit/list"),
                            menu_node("admin-property-house", "房屋管理", "/house/list"),
                            menu_node("admin-property-house-bind", "房产绑定", "/owner/list"),
                        ],
                    ),
                    menu_node(
                        "admin-property-parking",
                        "车位管理",
                        children=[
                            menu_node("admin-property-parking-info", "车位信息", "/parking/list"),
                            menu_node("admin-property-parking-bind", "车位绑定", "/parking/list"),
                            menu_node("admin-property-parking-status", "车位状态", "/parking/list"),
                            menu_node("admin-property-parking-temp", "临时停车", "/parking/list"),
                        ],
                    ),
                    menu_node(
                        "admin-property-visitor",
                        "访客管理",
                        children=[
                            menu_node("admin-property-visitor-list", "访客列表", "/visitor/list"),
                            menu_node("admin-property-visitor-create", "访客登记", "/visitor/create"),
                            menu_node("admin-property-visitor-approve", "访客审批", "/visitor/list"),
                        ],
                    ),
                    menu_node(
                        "admin-property-work-order",
                        "工单管理",
                        children=[
                            menu_node("admin-property-repair-order", "报修工单", "/repair/list"),
                            menu_node("admin-property-dispatch", "派单管理", "/repair/list"),
                            menu_node("admin-property-order-status", "工单状态", "/repair/list"),
                            menu_node("admin-property-order-rate", "工单评价", "/repair/list"),
                            menu_node("admin-property-order-stat", "工单统计", "/dashboard"),
                        ],
                    ),
                    menu_node(
                        "admin-property-notice",
                        "公告管理",
                        children=[
                            menu_node("admin-property-community-notice", "小区公告", "/notice/list"),
                            menu_node("admin-property-activity", "活动通知", "/notice/list"),
                            menu_node("admin-property-push", "消息推送", "/notice/list"),
                        ],
                    ),
                    menu_node(
                        "admin-property-complaint",
                        "投诉管理",
                        children=[
                            menu_node("admin-property-complaint-handle", "投诉处理", "/complaint/list"),
                            menu_node("admin-property-feedback", "建议反馈", "/complaint/list"),
                            menu_node("admin-property-return-visit", "回访记录", "/complaint/list"),
                        ],
                    ),
                    menu_node(
                        "admin-property-stat",
                        "数据统计",
                        children=[
                            menu_node("admin-property-user-stat", "用户统计", "/dashboard"),
                            menu_node("admin-property-fee-stat", "收费统计", "/dashboard"),
                            menu_node("admin-property-repair-stat", "工单统计", "/dashboard"),
                            menu_node("admin-property-chart", "可视化报表（优先显示在首页）", "/dashboard"),
                        ],
                    ),
                ],
            ),
        ],
    ),
    menu_node(
        "finance",
        "财务人员模块",
        children=[
            menu_node("finance-fee", "物业费管理", "/fee/list"),
            menu_node("finance-water", "水费管理", "/fee/list"),
            menu_node("finance-electric", "电费管理", "/fee/list"),
            menu_node("finance-parking", "停车费管理", "/fee/list"),
            menu_node("finance-pay", "在线支付", "/fee/list"),
            menu_node("finance-record", "缴费记录", "/fee/list"),
            menu_node("finance-arrears", "欠费提醒", "/fee/list"),
            menu_node("finance-report", "财务报表", "/dashboard"),
            menu_node("finance-income", "收入统计", "/dashboard"),
        ],
    ),
    menu_node(
        "repairer",
        "维修员模块",
        children=[
            menu_node("repairer-home", "首页", "/dashboard"),
            menu_node(
                "repairer-work-order",
                "工单管理",
                "/repair/list",
                [
                    menu_node("repairer-pending", "待接单工单", "/repair/list"),
                    menu_node("repairer-accepted", "已接单工单", "/repair/list"),
                    menu_node("repairer-fixing", "维修中工单", "/repair/list"),
                    menu_node("repairer-finished", "完成工单", "/repair/list"),
                    menu_node("repairer-history", "工单历史", "/repair/list"),
                ],
            ),
            menu_node("repairer-upload-image", "上传维修图片", "/repair/list"),
            menu_node("repairer-upload-result", "上传维修结果", "/repair/list"),
            menu_node("repairer-profile", "个人中心", "/profile"),
        ],
    ),
    menu_node(
        "owner",
        "业主模块",
        children=[
            menu_node(
                "owner-home",
                "首页",
                "/dashboard",
                [
                    menu_node("owner-home-notice", "公告通知", "/notice/list"),
                    menu_node("owner-home-activity", "小区活动", "/notice/list"),
                    menu_node("owner-home-fee", "代缴费用", "/fee/list"),
                    menu_node("owner-home-message", "消息提醒", "/message/center"),
                ],
            ),
            menu_node(
                "owner-profile",
                "个人中心",
                "/profile",
                children=[
                    menu_node("owner-realname", "实名认证", "/profile"),
                    menu_node("owner-phone", "手机号修改", "/profile"),
                    menu_node("owner-id-card-mask", "身份证脱敏显示", "/profile"),
                    menu_node("owner-password", "修改密码", "/profile"),
                    menu_node("owner-avatar", "头像上传", "/profile"),
                ],
            ),
            menu_node(
                "owner-house",
                "房产信息",
                "/house/list",
                [
                    menu_node("owner-house-my", "我的房屋", "/house/list"),
                    menu_node("owner-house-auth", "房产认证", "/owner/list"),
                    menu_node("owner-house-family", "家庭成员", "/owner/list"),
                    menu_node("owner-house-detail", "房屋详情", "/house/list"),
                ],
            ),
            menu_node(
                "owner-parking",
                "车位信息",
                "/parking/list",
                [
                    menu_node("owner-parking-my", "我的车位", "/parking/list"),
                    menu_node("owner-parking-record", "停车记录", "/parking/list"),
                    menu_node("owner-parking-pay", "停车缴费", "/fee/list"),
                ],
            ),
            menu_node(
                "owner-pay-center",
                "缴费中心",
                "/fee/list",
                [
                    menu_node("owner-pay-property", "物业费缴纳", "/fee/list"),
                    menu_node("owner-pay-water", "水费缴纳", "/fee/list"),
                    menu_node("owner-pay-electric", "电费缴纳", "/fee/list"),
                    menu_node("owner-pay-parking", "停车费缴纳", "/fee/list"),
                    menu_node("owner-pay-online", "在线支付", "/fee/list"),
                    menu_node("owner-pay-record", "缴费记录", "/fee/list"),
                ],
            ),
            menu_node(
                "owner-repair",
                "在线报修",
                "/repair/list",
                [
                    menu_node("owner-repair-submit", "提交报修", "/repair/create"),
                    menu_node("owner-repair-upload", "上传图片", "/repair/create"),
                    menu_node("owner-repair-progress", "工单进度", "/repair/list"),
                    menu_node("owner-repair-rate", "维修评价", "/repair/list"),
                    menu_node("owner-repair-history", "历史报修", "/repair/list"),
                ],
            ),
            menu_node(
                "owner-complaint",
                "在线投诉",
                children=[
                    menu_node("owner-complaint-submit", "提交投诉", "/complaint/create"),
                    menu_node("owner-complaint-progress", "投诉进度", "/complaint/list"),
                    menu_node("owner-complaint-result", "结果反馈", "/complaint/list"),
                    menu_node("owner-complaint-history", "历史投诉", "/complaint/list"),
                ],
            ),
            menu_node(
                "owner-message",
                "消息中心",
                "/message/center",
                children=[
                    menu_node("owner-message-system", "系统通知", "/message/center"),
                    menu_node("owner-message-fee", "缴费提醒", "/message/center"),
                    menu_node("owner-message-work-order", "工单通知", "/message/center"),
                    menu_node("owner-message-activity", "活动通知", "/message/center"),
                ],
            ),
        ],
    ),
    menu_node(
        "contact-service",
        "联系客服",
        "/contact/service",
    ),
    menu_node(
        "message",
        "消息通知模块",
        children=[
            menu_node("message-sms", "短信通知"),
            menu_node("message-notice", "系统公告", "/notice/list"),
            menu_node("message-work-order", "工单通知", "/repair/list"),
            menu_node("message-fee", "缴费提醒", "/fee/list"),
            menu_node("message-websocket", "WebSocket实时通知"),
            menu_node("message-mail", "站内信通知", "/message/center"),
        ],
    ),
    menu_node(
        "file",
        "文件管理模块",
        children=[
            menu_node("file-image", "图片上传", "/upload/test"),
            menu_node("file-id-card", "身份证上传", "/upload/test"),
            menu_node("file-repair-image", "工单图片上传", "/upload/test"),
            menu_node("file-oss", "OSS对象存储", "/upload/test", hidden=True),
            menu_node("file-security", "文件安全校验", "/upload/test", hidden=True),
        ],
    ),
    menu_node(
        "security",
        "系统安全模块",
        children=[
            menu_node("security-jwt", "JWT认证"),
            menu_node("security-redis", "Redis缓存"),
            menu_node("security-limit", "接口限流"),
            menu_node("security-sql", "SQL注入防护"),
            menu_node("security-xss", "XSS防护"),
            menu_node("security-csrf", "CSRF防护"),
            menu_node("security-mask", "敏感数据脱敏"),
            menu_node("security-audit-log", "操作审计日志", "/log/list"),
            menu_node("security-exception", "异常监控", "/dashboard"),
        ],
    ),
]


ROLE_DEFINITIONS = [
    {
        "code": "property_admin",
        "name": "物业管理员",
        "username": "property_admin_demo",
        "real_name": "物业管理员",
        "phone": "13800000001",
        "roots": [
            "rbac-user",
            "rbac-role",
            "rbac-permission",
            "admin-property",
            "contact-service",
        ],
        "is_staff": True,
    },
    {
        "code": "finance_staff",
        "name": "财务人员",
        "username": "finance_demo",
        "real_name": "财务人员",
        "phone": "13800000002",
        "roots": ["finance", "message", "contact-service"],
    },
    {
        "code": "repair_staff",
        "name": "维修员",
        "username": "repairer_demo",
        "real_name": "维修员",
        "phone": "13800000003",
        "roots": ["repairer", "message", "contact-service"],
    },
    {
        "code": "owner",
        "name": "业主",
        "username": "owner_demo",
        "real_name": "业主",
        "phone": "13800000004",
        "roots": ["owner", "contact-service"],
    },
    {
        "code": "customer_service",
        "name": "客服人员",
        "username": "customer_service_demo",
        "real_name": "客服人员",
        "phone": "13800000005",
        "roots": [],
    },
]


class Command(BaseCommand):
    help = "生成物业系统角色、菜单权限和演示账号；不会修改 superadmin。"

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep-password",
            action="store_true",
            help="已有演示账号不重置密码；默认会重置为本次输出的新密码。",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        menu_map = {}
        permission_map = {}

        for index, node in enumerate(MENU_TREE, start=1):
            self._sync_menu_node(node, None, index, 2, menu_map, permission_map)

        result = []
        User = get_user_model()

        for role_data in ROLE_DEFINITIONS:
            role, _ = Role.objects.get_or_create(
                code=role_data["code"],
                defaults={
                    "name": role_data["name"],
                },
            )

            role.name = role_data["name"]
            role.save(update_fields=["name"])

            permissions = []

            for root_code in role_data["roots"]:
                permissions.extend(self._collect_permissions(root_code, permission_map))

            role.permissions.set(permissions)

            password = f"Wy@{get_random_string(8)}2026"
            user, created = User.objects.get_or_create(
                username=role_data["username"],
                defaults={
                    "real_name": role_data["real_name"],
                    "is_active": True,
                    "is_staff": role_data.get("is_staff", False),
                    "status": 1,
                },
            )

            if user.is_superuser:
                raise CommandError(f"{user.username} 是超级管理员，命令已停止，未修改该账号。")

            phone_owner = User.objects.filter(phone=role_data["phone"]).exclude(id=user.id).first()

            if phone_owner:
                raise CommandError(
                    f"手机号 {role_data['phone']} 已被 {phone_owner.username} 使用，命令已停止。"
                )

            user.real_name = role_data["real_name"]
            user.phone = role_data["phone"]
            user.is_active = True
            user.is_staff = role_data.get("is_staff", False)
            user.status = 1
            user.role = role
            user.roles.set([role])

            if created or not options["keep_password"]:
                user.set_password(password)
            else:
                password = "未重置，沿用原密码"

            user.save()

            if role_data["code"] == "owner":
                self._ensure_owner_profile(user)

            result.append(
                {
                    "role": role.name,
                    "username": user.username,
                    "phone": user.phone,
                    "password": password,
                    "created": created,
                    "permission_count": len(permissions),
                }
            )

        self.stdout.write(
            json.dumps(
                {
                    "message": "角色账号生成完成，superadmin 未被修改",
                    "accounts": result,
                },
                ensure_ascii=False,
                indent=2,
            )
        )

    def _ensure_owner_profile(self, user):
        """给业主演示账号补齐业主资料，保证车位绑定和缴费流程可运行。"""

        if Owner.objects.filter(phone=user.phone).exists():
            return

        house = House.objects.order_by("id").first()

        if not house:
            return

        id_card_index = 1
        id_card = f"110101199001{id_card_index:06d}"

        while Owner.objects.filter(id_card=id_card).exists():
            id_card_index += 1
            id_card = f"110101199001{id_card_index:06d}"

        Owner.objects.create(
            house=house,
            name=user.real_name or user.username,
            phone=user.phone,
            relationship="self",
            id_card=id_card,
            gender="male",
            is_primary=False,
            status="approved",
            remark="演示账号自动补齐的业主资料",
        )

    def _sync_menu_node(
        self,
        node,
        parent,
        sort,
        level,
        menu_map,
        permission_map,
    ):
        menu_type = 2 if level >= 5 else 1
        menu, _ = Menu.objects.get_or_create(
            title=node["title"],
            parent=parent,
            defaults={
                "path": node.get("path"),
                "component": "",
                "sort": sort,
                "hidden": node.get("hidden", False),
                "menu_type": menu_type,
            },
        )

        menu.path = node.get("path")
        menu.sort = sort
        menu.hidden = node.get("hidden", False)
        menu.menu_type = menu_type
        menu.save(update_fields=["path", "sort", "hidden", "menu_type"])

        permission, _ = Permission.objects.get_or_create(
            code=f"menu:{node['code']}",
            defaults={
                "name": node["title"],
                "menu": menu,
            },
        )

        permission.name = node["title"]
        permission.menu = menu
        permission.save(update_fields=["name", "menu"])

        menu_map[node["code"]] = menu
        permission_map[node["code"]] = permission

        for child_index, child in enumerate(node.get("children", []), start=1):
            self._sync_menu_node(
                child,
                menu,
                child_index,
                level + 1,
                menu_map,
                permission_map,
            )

    def _collect_permissions(self, root_code, permission_map):
        prefix = f"{root_code}-"

        return [
            permission
            for code, permission in permission_map.items()
            if code == root_code or code.startswith(prefix)
        ]
