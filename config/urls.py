# 文件说明：汇总项目根路由，把各业务模块接口挂载到统一 API 前缀下。

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # 用户认证
    path("api/auth/", include("apps.users.urls.auth_urls")),
    path("api/menu/", include("apps.users.urls.menu_urls")),
    # 公告管理
    path(
        "api/notice/",
        include("apps.notice.urls"),
    ),
    path("api/permission/", include("apps.users.urls.permission_urls")),
    path("api/role/", include("apps.users.urls.role_urls")),
    path("api/user/", include("apps.users.urls.user_urls")),
    path("api/", include("apps.users.urls.auth_urls")),
    # 小区管理
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
    ),
    # 日志
    path(
        "api/log/",
        include("apps.logs.urls"),
    ),
    path(
        "api/",
        include("apps.upload.urls"),
    ),
    path(
        "api/visitor/",
        include("apps.visitors.urls.visitor_url"),
    ),
    path(
        "api/complaint/",
        include("apps.complaints.urls.complaint_urls"),
    ),
    path(
        "api/chat/",
        include("apps.chat.urls"),
    ),
]

# 开发环境文件访问

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
