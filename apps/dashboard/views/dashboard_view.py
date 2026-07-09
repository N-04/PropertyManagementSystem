# 文件说明：处理 apps/dashboard/views/dashboard_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework.views import APIView

from apps.community.models import House
from apps.finance.models import Fee
from apps.owners.models import Owner
from apps.parking.models import Parking
from apps.repairs.models import Repair
from apps.users.utils.role_access import get_user_role_codes
from apps.visitors.models import Visitor
from common.response.response import ResponseSuccess

MANAGER_ROLE_CODES = {
    "admin",
    "super_admin",
    "property_admin",
    "finance_staff",
}

VISITOR_MANAGER_ROLE_CODES = {
    "admin",
    "super_admin",
    "property_admin",
    "customer_service",
    "service",
}


def _owner_queryset_for_user(user):
    """按当前登录账号手机号定位业主资料，作为业主端数据隔离边界。"""

    phones = {item for item in [getattr(user, "phone", None), user.username] if item}
    return Owner.objects.filter(phone__in=phones)


def _build_dashboard_data(house_qs, owner_qs, parking_qs, repair_qs, fee_qs):
    """按传入查询集组装首页统计，确保所有统计都继承同一权限范围。"""

    fee_summary = fee_qs.aggregate(
        fee_total=Sum("amount"),
        fee_paid=Sum("amount", filter=Q(status="paid")),
        fee_unpaid=Sum("amount", filter=Q(status__in=["unpaid", "overdue"])),
        paid_count=Count("id", filter=Q(status="paid"), distinct=True),
        unpaid_count=Count(
            "id",
            filter=Q(status__in=["unpaid", "overdue"]),
            distinct=True,
        ),
    )
    repair_summary = repair_qs.aggregate(
        repair_count=Count("id", distinct=True),
        repair_pending=Count("id", filter=Q(status="pending"), distinct=True),
        repair_processing=Count(
            "id",
            filter=Q(status__in=["assigned", "accepted", "processing"]),
            distinct=True,
        ),
        repair_finished=Count("id", filter=Q(status="finished"), distinct=True),
    )

    return {
        "house_count": house_qs.distinct().count(),
        "owner_count": owner_qs.distinct().count(),
        "parking_count": parking_qs.distinct().count(),
        "repair_count": repair_summary["repair_count"],
        "fee_total": fee_summary["fee_total"] or 0,
        "fee_paid": fee_summary["fee_paid"] or 0,
        "fee_unpaid": fee_summary["fee_unpaid"] or 0,
        "repair_pending": repair_summary["repair_pending"],
        "repair_processing": repair_summary["repair_processing"],
        "repair_finished": repair_summary["repair_finished"],
        "paid_count": fee_summary["paid_count"],
        "unpaid_count": fee_summary["unpaid_count"],
    }


class DashboardView(APIView):
    """
    首页统计
    """

    def get(self, request):
        """
        获取首页统计数据
        """

        # 首页统计必须先判断角色，再按角色传入对应查询集，避免普通角色拿到全局数据。
        role_codes = get_user_role_codes(request.user)

        if role_codes & MANAGER_ROLE_CODES:
            # 管理端和财务端保留全局经营视角。
            data = _build_dashboard_data(
                House.objects.all(),
                Owner.objects.all(),
                Parking.objects.all(),
                Repair.objects.all(),
                Fee.objects.all(),
            )
        elif "owner" in role_codes:
            # 业主端只能看到自己手机号绑定的业务数据。
            owner_qs = _owner_queryset_for_user(request.user)
            house_qs = House.objects.filter(owners__in=owner_qs)
            data = _build_dashboard_data(
                house_qs,
                owner_qs,
                Parking.objects.filter(owner__in=owner_qs),
                Repair.objects.filter(owner__in=owner_qs),
                Fee.objects.filter(owner__in=owner_qs),
            )
        elif role_codes & {"repair_staff", "repairer", "repair"}:
            # 维修员只统计分配给自己的工单，不暴露全局房产和费用指标。
            repair_qs = Repair.objects.filter(repair_user=request.user)
            data = _build_dashboard_data(
                House.objects.none(),
                Owner.objects.none(),
                Parking.objects.none(),
                repair_qs,
                Fee.objects.none(),
            )
        else:
            # 其他角色没有首页汇总授权时返回空统计，保持响应结构稳定。
            data = _build_dashboard_data(
                House.objects.none(),
                Owner.objects.none(),
                Parking.objects.none(),
                Repair.objects.none(),
                Fee.objects.none(),
            )

        return ResponseSuccess(data=data)


class VisitorStatisticsView(APIView):
    """
    访客统计
    """

    def get(self, request):
        # 获取当前日期
        today = timezone.localdate()
        role_codes = get_user_role_codes(request.user)

        # 访客统计同样按角色隔离，防止维修/财务等角色看到全局访客状态。
        if role_codes & VISITOR_MANAGER_ROLE_CODES:
            # 只有访客管理侧角色可以看全局访客统计。
            visitor_qs = Visitor.objects.all()
        elif "owner" in role_codes:
            # 业主只统计访问自己的访客记录。
            visitor_qs = Visitor.objects.filter(
                owner__in=_owner_queryset_for_user(request.user)
            )
        else:
            # 财务、维修等无访客管理职责的角色不暴露全局访客状态。
            visitor_qs = Visitor.objects.none()

        # 今日来访数量
        today_count = visitor_qs.filter(visit_time__date=today).count()

        # 待审核数量
        waiting_count = visitor_qs.filter(status="waiting").count()

        # 已通过数量
        approved_count = visitor_qs.filter(status="approved").count()

        # 已到访数量
        entered_count = visitor_qs.filter(status="entered").count()

        # 已离开数量
        left_count = visitor_qs.filter(status="left").count()

        # 访客总数
        total_count = visitor_qs.count()

        return ResponseSuccess(
            data={
                "today_count": today_count,
                "waiting": waiting_count,
                "approved": approved_count,
                "entered": entered_count,
                "left": left_count,
                "total": total_count,
            }
        )
