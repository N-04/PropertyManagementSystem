# 文件说明：处理 apps/dashboard/views/dashboard_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView

from apps.community.models import House
from apps.finance.models import Fee
from apps.owners.models import Owner
from apps.parking.models import Parking
from apps.repairs.models import Repair
from apps.users.utils.role_access import get_user_role_codes
from django.db.models import Sum
from django.utils import timezone

from apps.visitors.models import Visitor
from common.response.response import ResponseSuccess


MANAGER_ROLE_CODES = {
    "admin",
    "super_admin",
    "property_admin",
    "finance_staff",
}


def _money_total(queryset):
    """汇总金额字段，空结果统一返回 0，避免前端出现 null。"""

    return queryset.aggregate(total=Sum("amount"))["total"] or 0


def _owner_queryset_for_user(user):
    """按当前登录账号手机号定位业主资料，作为业主端数据隔离边界。"""

    phones = {item for item in [getattr(user, "phone", None), user.username] if item}
    return Owner.objects.filter(phone__in=phones)


def _build_dashboard_data(house_qs, owner_qs, parking_qs, repair_qs, fee_qs):
    """按传入查询集组装首页统计，确保所有统计都继承同一权限范围。"""

    paid_fee_qs = fee_qs.filter(status="paid")
    unpaid_fee_qs = fee_qs.filter(status__in=["unpaid", "overdue"])

    return {
        "house_count": house_qs.distinct().count(),
        "owner_count": owner_qs.distinct().count(),
        "parking_count": parking_qs.distinct().count(),
        "repair_count": repair_qs.distinct().count(),
        "fee_total": _money_total(fee_qs),
        "fee_paid": _money_total(paid_fee_qs),
        "fee_unpaid": _money_total(unpaid_fee_qs),
        "repair_pending": repair_qs.filter(status="pending").distinct().count(),
        "repair_processing": repair_qs.filter(
            status__in=["assigned", "accepted", "processing"]
        )
        .distinct()
        .count(),
        "repair_finished": repair_qs.filter(status="finished").distinct().count(),
        "paid_count": paid_fee_qs.distinct().count(),
        "unpaid_count": unpaid_fee_qs.distinct().count(),
    }


class DashboardView(APIView):
    """
    首页统计
    """

    def get(self, request):
        """
        获取首页统计数据
        """

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

        # 今日来访数量
        today_count = Visitor.objects.filter(visit_time__date=today).count()

        # 待审核数量
        waiting_count = Visitor.objects.filter(status="waiting").count()

        # 已通过数量
        approved_count = Visitor.objects.filter(status="approved").count()

        # 已到访数量
        entered_count = Visitor.objects.filter(status="entered").count()

        # 已离开数量
        left_count = Visitor.objects.filter(status="left").count()

        # 访客总数
        total_count = Visitor.objects.count()

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
