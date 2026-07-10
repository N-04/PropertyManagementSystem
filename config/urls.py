# 文件说明：汇总项目根路由，把各业务模块接口挂载到统一 API 前缀下。

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path, re_path


def api_root(_request):
    return JsonResponse(
        {
            "name": "Property Management System API",
            "status": "ok",
            "endpoints": {
                "auth": "/api/auth/",
                "menu": "/api/menu/",
                "notice": "/api/notice/",
                "permission": "/api/permission/",
                "role": "/api/role/",
                "user": "/api/user/",
                "community": "/api/community/",
                "building": "/api/building/",
                "unit": "/api/unit/",
                "house": "/api/house/",
                "owner": "/api/owner/",
                "parking": "/api/parking/",
                "car": "/api/car/",
                "repair": "/api/repair/",
                "fee": "/api/fee/",
                "dashboard": "/api/dashboard/",
                "log": "/api/log/",
                "upload": "/api/upload/",
                "visitor": "/api/visitor/",
                "complaint": "/api/complaint/",
                "chat": "/api/chat/",
            },
        }
    )

urlpatterns = [
    path("admin/", admin.site.urls),  # Django 管理后台入口。
    re_path(r"^api/?$", api_root),  # API 根路径，便于浏览器直接访问和部署健康检查。
    # 认证路由使用 /api/auth/ 作为唯一前端调用前缀。
    path("api/auth/", include("apps.users.urls.auth_urls")),
    # RBAC 分块：菜单、权限、角色和用户管理按资源独立挂载。
    path("api/menu/", include("apps.users.urls.menu_urls")),
    path(
        "api/notice/",
        include("apps.notice.urls"),
    ),  # 公告管理接口。
    path("api/permission/", include("apps.users.urls.permission_urls")),
    path("api/role/", include("apps.users.urls.role_urls")),
    path("api/user/", include("apps.users.urls.user_urls")),
    # 小区管理保留在 /api/ 下，是因为内部 urls 已经带 building/unit/house 等资源前缀。
    path(
        "api/",
        include("apps.community.urls"),
    ),
    # 业主管理
    path(
        "api/owner/",
        include("apps.owners.urls"),
    ),
    # 车位管理
    path("api/parking/", include("apps.parking.urls.parking_urls")),
    # 车辆管理
    path(
        "api/car/",
        include("apps.cars.urls.cars_url"),
    ),
    # 维修管理
    path(
        "api/repair/",
        include("apps.repairs.urls.repair_url"),
    ),
    # 物业费管理
    path(
        "api/fee/",
        include("apps.finance.urls"),
    ),
    # 首页统计
    path(
        "api/dashboard/",
        include("apps.dashboard.urls"),
    ),  # 首页工作台和统计接口。
    path(
        "api/log/",
        include("apps.logs.urls"),
    ),  # 操作日志和登录日志接口。
    # 上传接口内部使用 upload/ 前缀，统一挂在 /api/upload/。
    path(
        "api/",
        include("apps.upload.urls"),
    ),
    path(
        "api/visitor/",
        include("apps.visitors.urls.visitor_url"),
    ),  # 访客通行接口。
    path(
        "api/complaint/",
        include("apps.complaints.urls.complaint_urls"),
    ),  # 投诉建议接口。
    path(
        "api/chat/",
        include("apps.chat.urls"),
    ),  # 角色消息会话接口。
]

# 开发环境文件访问分块：DEBUG 下让浏览器能访问本地上传的媒体文件。
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
