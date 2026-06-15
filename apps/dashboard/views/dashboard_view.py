# 文件说明：处理 apps/dashboard/views/dashboard_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from rest_framework.views import APIView

from apps.community.models import House
from apps.owners.models import Owner
from apps.parking.models import Parking
from apps.repairs.models import Repair
from apps.finance.models import Fee
from django.db.models import Count
from django.utils import timezone

from apps.visitors.models import Visitor
from common.response.response import ResponseSuccess


class DashboardView(APIView):
    """
    首页统计
    """

    def get(self, request):
        """
        获取首页统计数据
        """

        # =========================
        # 房屋总数
        # =========================
        house_count = House.objects.count()

        # =========================
        # 业主总数
        # =========================
        owner_count = Owner.objects.count()

        # =========================
        # 车位总数
        # =========================
        parking_count = Parking.objects.count()

        # =========================
        # 报修总数
        # =========================
        repair_count = Repair.objects.count()

        # =========================
        # 物业费总额
        # =========================
        fee_total = sum(
            Fee.objects.values_list(
                "amount",
                flat=True,
            )
        )

        # =========================
        # 已缴费金额
        # =========================
        fee_paid = sum(
            Fee.objects.filter(status="paid").values_list(
                "amount",
                flat=True,
            )
        )

        # =========================
        # 未缴费金额
        # =========================
        fee_unpaid = sum(
            Fee.objects.filter(status="unpaid").values_list(
                "amount",
                flat=True,
            )
        )

        # =========================
        # 待派单报修
        # =========================
        repair_pending = Repair.objects.filter(status="pending").count()

        # =========================
        # 进行中报修：包含待接单、已接单和维修中
        # =========================
        repair_processing = Repair.objects.filter(
            status__in=["assigned", "accepted", "processing"]
        ).count()

        # =========================
        # 已完成报修
        # =========================
        repair_finished = Repair.objects.filter(status="finished").count()

        # 已缴费账单数
        paid_count = Fee.objects.filter(status="paid").count()

        # 未缴费账单数
        unpaid_count = Fee.objects.filter(status="unpaid").count()

        # =========================
        # 返回统计结果
        # =========================
        return ResponseSuccess(
            data={
                # 基础统计:房屋数量,业主数量,车位数量,报修数量
                "house_count": house_count,
                "owner_count": owner_count,
                "parking_count": parking_count,
                "repair_count": repair_count,
                # 费用统计:物业费总额,已缴费金额,未缴费金额
                "fee_total": fee_total,
                "fee_paid": fee_paid,
                "fee_unpaid": fee_unpaid,
                # 报修统计:
                "repair_pending": repair_pending,
                "repair_processing": repair_processing,
                "repair_finished": repair_finished,
                # 账单统计:已缴费账单数,未缴费账单数
                "paid_count": paid_count,
                "unpaid_count": unpaid_count,
            }
        )


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
