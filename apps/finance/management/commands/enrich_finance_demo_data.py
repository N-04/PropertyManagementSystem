# 文件说明：补齐演示数据空字段，并生成可用于财务图表的真实关联账单数据。

import calendar
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.community.models import Building, Community, House, Unit
from apps.finance.models import Fee
from apps.owners.models import Owner
from apps.parking.models import Parking


HOUSE_TYPES = ("一室一厅", "两室一厅", "两室两厅", "三室一厅", "三室两厅", "四室两厅")
RELATIONSHIP_TEXT = {
    "self": "本人",
    "spouse": "配偶",
    "child": "子女",
    "parent": "父母",
    "other": "其他",
}
FEE_TYPE_TEXT = dict(Fee.TYPE_CHOICES)
PAYMENT_METHODS = ("alipay", "wechat", "bank_card", "apple_pay", "union_pay")
PAYMENT_METHOD_TEXT = dict(Fee.PAYMENT_METHOD_CHOICES)


def money(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def parse_birthday(id_card):
    if not id_card or len(id_card) < 14:
        return None
    birthday_text = id_card[6:14]
    if not birthday_text.isdigit():
        return None
    try:
        return datetime.strptime(birthday_text, "%Y%m%d").date()
    except ValueError:
        return None


def month_deadline(base_date, offset):
    month_index = base_date.month - 1 + offset
    year = base_date.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    deadline = datetime(year, month, last_day, 23, 59, 59)
    return timezone.make_aware(deadline, timezone.get_current_timezone())


def random_phone(prefix="13"):
    return f"{prefix}{random.randint(100000000, 999999999)}"


def random_payment_time(deadline, now):
    latest = min(deadline, now)
    earliest = latest - timedelta(days=random.randint(1, 18), hours=random.randint(0, 8))
    return earliest.replace(
        hour=random.randint(8, 21),
        minute=random.choice((0, 5, 10, 15, 20, 30, 35, 40, 45, 50)),
        second=0,
        microsecond=0,
    )


class Command(BaseCommand):
    help = "补齐演示数据空字段，并生成可支撑财务统计图表的真实费用账单。"

    def add_arguments(self, parser):
        parser.add_argument("--months", type=int, default=8, help="按最近多少个月生成账单，默认 8。")
        parser.add_argument("--owners", type=int, default=260, help="最多参与生成账单的业主数，默认 260。")
        parser.add_argument("--paid-today", type=int, default=80, help="补充为今日已缴费的记录数，默认 80。")
        parser.add_argument("--seed", type=int, default=20260703, help="随机种子，默认 20260703。")

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(options["seed"])
        months = max(1, options["months"])
        owner_limit = max(1, options["owners"])
        paid_today_target = max(0, options["paid_today"])

        updated_counts = self.fill_blank_values()
        owners = self.get_billable_owners(owner_limit)
        if not owners:
            raise CommandError("没有找到带房屋关联的业主，无法生成真实费用账单。")

        created_count, normalized_count = self.ensure_fee_rows(owners, months)
        paid_today_count = self.ensure_today_paid_records(paid_today_target)

        self.stdout.write(self.style.SUCCESS("演示财务数据补齐完成"))
        self.stdout.write(f"补齐空字段：{updated_counts}")
        self.stdout.write(f"参与业主：{len(owners)}")
        self.stdout.write(f"新增账单：{created_count}")
        self.stdout.write(f"规范化账单：{normalized_count}")
        self.stdout.write(f"今日已缴补充：{paid_today_count}")

    def fill_blank_values(self):
        counts = {
            "community": 0,
            "building": 0,
            "unit": 0,
            "house": 0,
            "owner": 0,
            "parking": 0,
        }

        for community in Community.objects.all():
            fields = []
            if not community.address:
                community.address = f"杭州市西湖区{community.name}"
                fields.append("address")
            if not community.contact_name:
                community.contact_name = random.choice(("陈经理", "王主管", "李主任", "赵经理"))
                fields.append("contact_name")
            if not community.contact_phone:
                community.contact_phone = random_phone("18")
                fields.append("contact_phone")
            if community.remark in (None, ""):
                community.remark = f"{community.name}社区物业管理演示数据"
                fields.append("remark")
            if fields:
                community.save(update_fields=fields)
                counts["community"] += 1

        for building in Building.objects.select_related("community"):
            fields = []
            unit_count = building.units.count()
            if not building.floor_count:
                building.floor_count = random.choice((18, 24, 26, 30, 32))
                fields.append("floor_count")
            if not building.unit_count and unit_count:
                building.unit_count = unit_count
                fields.append("unit_count")
            if fields:
                building.save(update_fields=fields)
                counts["building"] += 1

        for unit in Unit.objects.select_related("building"):
            if not unit.floor_count:
                unit.floor_count = unit.houses.count() or random.choice((18, 24, 26, 30))
                unit.save(update_fields=["floor_count"])
                counts["unit"] += 1

        for house in House.objects.select_related("unit__building__community"):
            fields = []
            owner_count = house.owners.count()
            if not house.area or house.area <= 0:
                house.area = money(random.uniform(78, 142))
                fields.append("area")
            if not house.house_type:
                house.house_type = random.choice(HOUSE_TYPES)
                fields.append("house_type")
            target_status = "occupied" if owner_count else "vacant"
            if house.status != target_status:
                house.status = target_status
                fields.append("status")
            if house.owner_count != owner_count:
                house.owner_count = owner_count
                fields.append("owner_count")
            target_resident_count = owner_count if owner_count == 0 else max(owner_count, random.randint(1, 4))
            if house.resident_count != target_resident_count:
                house.resident_count = target_resident_count
                fields.append("resident_count")
            if house.remark in (None, ""):
                community_name = house.unit.building.community.name
                house.remark = f"{community_name}{house.unit.building.name}{house.unit.name}{house.room_no}房屋资料"
                fields.append("remark")
            if fields:
                house.save(update_fields=fields)
                counts["house"] += 1

        for owner in Owner.objects.select_related("house__unit__building__community"):
            fields = []
            if not owner.gender:
                owner.gender = random.choice(("male", "female"))
                fields.append("gender")
            if not owner.birthday:
                owner.birthday = parse_birthday(owner.id_card) or datetime(
                    random.randint(1970, 1998),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ).date()
                fields.append("birthday")
            if owner.remark in (None, ""):
                relation = RELATIONSHIP_TEXT.get(owner.relationship, "家庭成员")
                house_text = owner.house.room_no if owner.house_id else "未绑定房屋"
                owner.remark = f"{relation}，{house_text}住户资料"
                fields.append("remark")
            if fields:
                owner.save(update_fields=fields)
                counts["owner"] += 1

        for parking in Parking.objects.select_related("owner"):
            fields = []
            if not parking.area or parking.area <= 0:
                parking.area = Decimal("12.50")
                fields.append("area")
            target_status = "used" if parking.owner_id else "idle"
            if parking.status != target_status:
                parking.status = target_status
                fields.append("status")
            if fields:
                parking.save(update_fields=fields)
                counts["parking"] += 1

        return counts

    def get_billable_owners(self, limit):
        primary_owners = list(
            Owner.objects.select_related("house")
            .filter(house__isnull=False, is_primary=True)
            .order_by("id")[:limit]
        )
        if len(primary_owners) >= limit:
            return primary_owners

        existing_ids = {owner.id for owner in primary_owners}
        other_owners = (
            Owner.objects.select_related("house")
            .filter(house__isnull=False)
            .exclude(id__in=existing_ids)
            .order_by("id")[: limit - len(primary_owners)]
        )
        return primary_owners + list(other_owners)

    def ensure_fee_rows(self, owners, months):
        now = timezone.now()
        offsets = self.month_offsets(months)
        created_count = 0
        normalized_count = 0

        for owner in owners:
            if not owner.house_id:
                continue
            fee_types = ["property", "water", "electric"]
            if owner.parkings.exists():
                fee_types.append("parking")
            for offset in offsets:
                deadline = month_deadline(now.date(), offset)
                for fee_type in fee_types:
                    fee = Fee.objects.filter(
                        owner=owner,
                        house=owner.house,
                        fee_type=fee_type,
                        deadline__year=deadline.year,
                        deadline__month=deadline.month,
                    ).first()
                    if fee:
                        normalized_count += self.normalize_fee(fee, now)
                        continue
                    Fee.objects.create(
                        owner=owner,
                        house=owner.house,
                        fee_type=fee_type,
                        amount=self.calc_fee_amount(owner, fee_type),
                        deadline=deadline,
                        **self.payment_fields(deadline, now),
                        remark=self.build_remark(owner, fee_type),
                    )
                    created_count += 1

        return created_count, normalized_count

    def month_offsets(self, months):
        past_months = max(months - 2, 1)
        offsets = list(range(-past_months, 2))
        return offsets[-months:]

    def calc_fee_amount(self, owner, fee_type):
        area = money(owner.house.area or 90)
        if fee_type == "property":
            return money(area * Decimal(str(random.uniform(2.4, 3.6))))
        if fee_type == "water":
            return money(random.uniform(48, 168))
        if fee_type == "electric":
            return money(random.uniform(86, 360))
        if fee_type == "parking":
            return money(random.uniform(220, 360))
        return money(random.uniform(30, 120))

    def pick_status(self, deadline, now):
        if deadline < now:
            return random.choices(("paid", "overdue"), weights=(72, 28), k=1)[0]
        if deadline.year == now.year and deadline.month == now.month:
            return random.choices(("paid", "unpaid"), weights=(42, 58), k=1)[0]
        return "unpaid"

    def payment_fields(self, deadline, now):
        status = self.pick_status(deadline, now)
        if status != "paid":
            return {"status": status, "payment_method": None, "pay_time": None}
        return {
            "status": "paid",
            "payment_method": random.choice(PAYMENT_METHODS),
            "pay_time": random_payment_time(deadline, now),
        }

    def normalize_fee(self, fee, now):
        fields = []
        if fee.status == "paid":
            if not fee.payment_method:
                fee.payment_method = random.choice(PAYMENT_METHODS)
                fields.append("payment_method")
            if not fee.pay_time:
                fee.pay_time = random_payment_time(fee.deadline, now)
                fields.append("pay_time")
        else:
            if fee.deadline < now and fee.status == "unpaid":
                fee.status = "overdue"
                fields.append("status")
            if fee.pay_time:
                fee.pay_time = None
                fields.append("pay_time")
            if fee.payment_method:
                fee.payment_method = None
                fields.append("payment_method")
        if fee.remark in (None, ""):
            fee.remark = self.build_remark(fee.owner, fee.fee_type)
            fields.append("remark")
        if fields:
            fee.save(update_fields=fields)
            return 1
        return 0

    def build_remark(self, owner, fee_type):
        fee_name = FEE_TYPE_TEXT.get(fee_type, "费用")
        if fee_type == "parking":
            parking = owner.parkings.order_by("id").first()
            parking_no = parking.parking_no if parking else "未绑定车位"
            return f"{fee_name}：{parking_no}"
        if owner.house_id:
            return f"{owner.house.unit.building.name}{owner.house.unit.name}{owner.house.room_no} {fee_name}"
        return fee_name

    def ensure_today_paid_records(self, target_count):
        if target_count == 0:
            return 0
        today = timezone.localdate()
        now = timezone.now()
        current_month_fees = list(
            Fee.objects.filter(deadline__year=today.year, deadline__month=today.month)
            .exclude(status="paid")
            .order_by("id")
        )
        random.shuffle(current_month_fees)
        selected_fees = current_month_fees[:target_count]

        for index, fee in enumerate(selected_fees):
            fee.status = "paid"
            fee.payment_method = PAYMENT_METHODS[index % len(PAYMENT_METHODS)]
            fee.pay_time = now.replace(
                hour=random.randint(8, 18),
                minute=random.choice((0, 10, 20, 30, 40, 50)),
                second=0,
                microsecond=0,
            )
            if not fee.remark:
                method_name = PAYMENT_METHOD_TEXT.get(fee.payment_method, "在线支付")
                fee.remark = f"{self.build_remark(fee.owner, fee.fee_type)}，{method_name}已缴"
            fee.save(update_fields=["status", "payment_method", "pay_time", "remark"])

        return len(selected_fees)
