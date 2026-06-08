from rest_framework.views import APIView

from apps.community.models import House
from apps.owners.models import Owner
from apps.parking.models import Parking
from apps.repairs.models import Repair
from apps.finance.models import Fee

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
        # 待处理报修
        # =========================
        repair_pending = Repair.objects.filter(status="pending").count()

        # =========================
        # 处理中报修
        # =========================
        repair_processing = Repair.objects.filter(status="processing").count()

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
