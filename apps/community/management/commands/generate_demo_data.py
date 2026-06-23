# 文件说明：提供 Django 管理命令，用于维护或生成项目数据。

from datetime import datetime
from decimal import Decimal
import random
import string

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from faker import Faker

from apps.community.models.community import Community
from apps.community.models.building import Building
from apps.community.models.unit import Unit
from apps.community.models.house import House

from apps.owners.models.owner import Owner
from apps.owners.services.owner_account_service import ensure_owner_login_user
from apps.parking.models.parking import Parking
from apps.cars.models import Car
from apps.visitors.models.visitor import Visitor
from apps.finance.models.fee import Fee

fake = Faker("zh_CN")

DEMO_COMMUNITIES = [
    {
        "name": "一期社区",
        "code": "PHASE001",
        "address": "杭州市西湖区幸福里一期",
        "contact_name": "周管家",
        "contact_phone": "0571-6386-9274",
    },
    {
        "name": "二期社区",
        "code": "PHASE002",
        "address": "杭州市西湖区幸福里二期",
        "contact_name": "陈管家",
        "contact_phone": "0571-5824-1396",
    },
]

FAMILY_TEMPLATES = [
    ("self", "spouse"),
    ("self", "spouse", "child"),
    ("self", "spouse", "child", "parent"),
    ("self", "parent"),
]

RELATIONSHIP_LABELS = {
    "self": "本人",
    "spouse": "配偶",
    "child": "子女",
    "parent": "父母",
    "other": "其他",
}

FEE_TYPE_AMOUNT_RULES = {
    "property": (Decimal("2.80"), Decimal("4.20")),
    "water": (Decimal("40.00"), Decimal("180.00")),
    "electric": (Decimal("80.00"), Decimal("420.00")),
    "parking": (Decimal("180.00"), Decimal("320.00")),
}


class Command(BaseCommand):

    help = "生成物业管理演示数据"

    def add_arguments(self, parser):

        parser.add_argument(
            "--reset",
            action="store_true",
            help="删除旧数据重新生成",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.used_phone = set()
        self.used_id_card = set()
        self.used_plate = set()

        self.used_phone.update(
            Owner.objects.exclude(phone__isnull=True).values_list("phone", flat=True)
        )
        self.used_id_card.update(
            Owner.objects.exclude(id_card__isnull=True).values_list("id_card", flat=True)
        )
        self.used_plate.update(
            Car.objects.exclude(plate_no__isnull=True).values_list("plate_no", flat=True)
        )

        if options["reset"]:

            self.stdout.write("正在清空旧数据...")

            Fee.objects.all().delete()
            Visitor.objects.all().delete()
            Car.objects.all().delete()
            Parking.objects.all().delete()
            Owner.objects.all().delete()

            House.objects.all().delete()
            Unit.objects.all().delete()
            Building.objects.all().delete()
            Community.objects.all().delete()

            self.stdout.write(self.style.SUCCESS("旧数据清理完成"))

        if House.objects.exists():

            self.stdout.write(
                self.style.WARNING(
                    "数据库已有数据，如需重新生成请执行："
                    "\npython manage.py generate_demo_data --reset"
                )
            )

            return

        self.stdout.write(self.style.SUCCESS("开始生成演示数据..."))

        self.stdout.write("生成小区...")

        self.communities = []

        for community_data in DEMO_COMMUNITIES:

            community = Community.objects.create(
                name=community_data["name"],
                code=community_data["code"],
                address=community_data["address"],
                contact_name=community_data["contact_name"],
                contact_phone=community_data["contact_phone"],
            )

            self.communities.append(community)

        self.stdout.write("√ 小区完成")

        # ==========================
        # 生成楼栋
        # ==========================

        self.stdout.write("生成楼栋...")

        self.buildings = []

        for community in self.communities:

            for b in range(1, 7):

                building = Building.objects.create(
                    community=community,
                    name=f"{b}栋",
                    code=f"{community.code}-B{b:02d}",
                    floor_count=18,
                    unit_count=2,
                )

                self.buildings.append(building)

        self.stdout.write("√ 楼栋完成")

        # ==========================
        # 生成单元
        # ==========================

        self.stdout.write("生成单元...")

        self.units = []

        for building in self.buildings:

            for u in range(1, 3):

                unit = Unit.objects.create(
                    building=building,
                    name=f"{u}单元",
                    code=f"{building.code}-U{u:02d}",
                    floor_count=18,
                )

                self.units.append(unit)

        self.stdout.write("√ 单元完成")

        # ==========================
        # 生成房屋
        # ==========================

        self.stdout.write("生成房屋...")

        self.houses = []

        for unit in self.units:

            for floor in range(1, 19):

                for room in range(1, 5):

                    house = House.objects.create(
                        unit=unit,
                        room_no=f"{floor:02d}{room:02d}",
                        area=random.randint(80, 160),
                        house_type=random.choice(
                            [
                                "两室一厅",
                                "三室一厅",
                                "三室两厅",
                                "四室两厅",
                            ]
                        ),
                        status=random.choice(
                            [
                                "occupied",
                                "renting",
                                "repairing",
                                "vacant",
                            ]
                        ),
                        owner_count=0,
                        resident_count=0,
                    )

                    self.houses.append(house)

        self.stdout.write(
            self.style.SUCCESS(f"√ 房屋完成，共生成 {len(self.houses)} 套")
        )

        # ==========================
        # 生成业主
        # ==========================

        self.stdout.write("生成业主...")

        self.owners = []

        User = get_user_model()
        demo_owner_user = (
            User.objects.filter(username="owner_dem").first()
            or User.objects.filter(username="owner_demo").first()
        )

        for house_index, house in enumerate(self.houses):
            relationships = self.select_house_family(house, house_index)

            for index, relationship in enumerate(relationships):
                owner_name = self.generate_family_member_name(relationship)
                owner_phone = self.generate_phone()

                if house_index == 0 and relationship == "self" and demo_owner_user:
                    owner_name = demo_owner_user.real_name or demo_owner_user.username
                    owner_phone = demo_owner_user.phone or owner_phone

                owner = Owner.objects.create(
                    house=house,
                    name=owner_name,
                    phone=owner_phone,
                    relationship=relationship,
                    gender=self.generate_gender(relationship),
                    birthday=self.generate_birthday(relationship),
                    id_card=self.generate_id_card(relationship),
                    is_primary=(index == 0),
                    status="approved",
                    remark=f"系统生成演示数据：{RELATIONSHIP_LABELS[relationship]}",
                )

                self.owners.append(owner)

                if owner.is_primary:
                    ensure_owner_login_user(owner)

            house.owner_count = len(relationships)
            house.resident_count = 0 if house.status == "vacant" else len(relationships)
            house.save(update_fields=["owner_count", "resident_count"])

        self.stdout.write(
            self.style.SUCCESS(f"√ 业主完成，共生成 {len(self.owners)} 人")
        )

        self.stdout.write("生成车位")
        self.parkings = []

        parking_index = 1

        for owner in self.owners:
            if not owner.is_primary:
                continue

            # 70%的业主拥有车位
            if random.random() < 0.7:
                parking = Parking.objects.create(
                    owner=owner,
                    # f""格式化字符串，P为开头，格式化车位号，实际位数不足5位用0补齐，最终显示总宽度为5位，十进制表示
                    parking_no=f"P{parking_index:05d}",
                    # 面积在12-20之间
                    area=random.randint(12, 20),
                    status="used",
                )
                self.parkings.append(parking)
                parking_index += 1
        self.stdout.write(
            self.style.SUCCESS(f"√ 车位完成，共生成 {len(self.parkings)} 个")
        )

        # 生成车辆
        self.stdout.write("生成车辆...")
        brands = [
            "比亚迪",
            "特斯拉",
            "宝马",
            "奔驰",
            "奥迪",
            "大众",
            "丰田",
            "本田",
            "理想",
            "蔚来",
            "小鹏",
            "小米",
            "红旗",
        ]

        colors = [
            "白色",
            "黑色",
            "灰色",
            "银色",
            "蓝色",
            "红色",
        ]

        self.cars = []

        for parking in self.parkings:
            # 80%的车位有车
            if random.random() < 0.8:
                car = Car.objects.create(
                    owner=parking.owner,
                    parking=parking,
                    # 随机分配一个车位
                    brand=random.choice(brands),
                    # 随机生成车牌号
                    plate_no=self.generate_plate(),
                    # 随机分配颜色
                    color=random.choice(colors),
                    car_type="monthly",
                    status="normal",
                )
                self.cars.append(car)

        self.stdout.write(self.style.SUCCESS(f"√ 车辆完成，共生成 {len(self.cars)} 辆"))

        #     生成访客
        self.stdout.write("生成访客")
        self.visitors = []
        visitor_sample_size = min(300, len(self.owners))

        for owner in random.sample(self.owners, visitor_sample_size):
            status = random.choice(
                [
                    "waiting",
                    "approved",
                    "rejected",
                    "entered",
                    "left",
                ]
            )
            visitor = Visitor.objects.create(
                owner=owner,
                name=fake.name(),
                phone=self.generate_phone(),
                id_card=self.generate_id_card(),
                reason=random.choice(
                    [
                        "探亲",
                        "送货",
                        "维修",
                        "聚会",
                        "拜访朋友",
                    ]
                ),
                # “注入”指定的时区信息
                visit_time=timezone.make_aware(
                    fake.date_time_between(
                        start_date="-30d",
                        end_date="+7d",
                    )
                ),
                status=status,
            )
            if visitor.status in ["approved", "entered", "left"]:
                visitor.approve_time = timezone.now()
            if visitor.status in ["entered", "left"]:
                visitor.enter_time = timezone.now()
            if visitor.status == "left":
                visitor.leave_time = timezone.now()
            visitor.save(update_fields=["approve_time", "enter_time", "leave_time"])
            self.visitors.append(visitor)

        self.stdout.write(
            self.style.SUCCESS(f"√ 访客完成，共生成 {len(self.visitors)} 人")
        )

        self.stdout.write("生成物业费...")

        self.fees = []

        primary_owners = [owner for owner in self.owners if owner.is_primary]

        for owner in primary_owners:
            for month_offset in [-1, 0, 1]:
                for fee_type in self.get_owner_fee_types(owner):
                    amount = self.generate_fee_amount(owner.house, fee_type)
                    deadline = self.generate_fee_deadline(month_offset)
                    status = self.generate_fee_status(deadline)

                    fee = Fee.objects.create(
                        owner=owner,
                        house=owner.house,
                        amount=amount,
                        fee_type=fee_type,
                        deadline=deadline,
                        status=status,
                        pay_time=(timezone.now() if status == "paid" else None),
                        payment_method=(
                            random.choice(["alipay", "wechat", "bank_card"])
                            if status == "paid"
                            else None
                        ),
                        remark="系统自动生成",
                    )
                    self.fees.append(fee)
        self.stdout.write(
            self.style.SUCCESS(f"√ 物业费完成，共生成 {len(self.fees)} 条")
        )

    #     生成手机号
    def generate_phone(self):

        while True:

            phone = "1" + random.choice(["3", "4", "5", "6", "7", "8", "9"])

            phone += "".join(random.choice(string.digits) for _ in range(9))

            if phone not in self.used_phone:

                self.used_phone.add(phone)

                return phone

    #         生成身份证
    def generate_id_card(self, relationship="self"):

        while True:

            birth_date = self.generate_birthday(relationship)
            body = (
                "110101"
                + birth_date.strftime("%Y%m%d")
                + f"{random.randint(100,999):03d}"
            )
            card = body + self.generate_id_card_check_digit(body)

            if card not in self.used_id_card:

                self.used_id_card.add(card)

                return card

    #         生成车牌
    def generate_plate(self):

        while True:

            plate = "京"

            plate += random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ")

            plate += "".join(
                random.choice(string.digits + "ABCDEFGHJKLMNPQRSTUVWXYZ")
                for _ in range(5)
            )

            if plate not in self.used_plate:

                self.used_plate.add(plate)

                return plate

    def select_house_family(self, house, house_index):
        """按房屋状态生成家庭关系，首套房优先给演示业主账号形成稳定数据。"""

        if house_index == 0:
            return ["self", "spouse", "child"]

        if house.status == "vacant":
            return ["self"]

        return list(random.choice(FAMILY_TEMPLATES))

    def generate_family_member_name(self, relationship):
        if relationship == "child":
            return fake.first_name() + random.choice(["小朋友", "同学"])

        return fake.name()

    def generate_gender(self, relationship):
        if relationship == "spouse":
            return random.choice(["male", "female"])

        return random.choice(["male", "female"])

    def generate_birthday(self, relationship):
        if relationship == "child":
            return fake.date_between(start_date="-16y", end_date="-6y")

        if relationship == "parent":
            return fake.date_between(start_date="-75y", end_date="-50y")

        return fake.date_between(start_date="-60y", end_date="-22y")

    def generate_id_card_check_digit(self, body):
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_digits = "10X98765432"
        total = sum(int(number) * weight for number, weight in zip(body, weights))

        return check_digits[total % 11]

    def get_owner_fee_types(self, owner):
        fee_types = ["property", "water", "electric"]

        if owner.parkings.exists():
            fee_types.append("parking")

        return fee_types

    def generate_fee_amount(self, house, fee_type):
        if fee_type == "property":
            amount = Decimal(house.area) * Decimal(str(random.uniform(2.8, 4.2)))
        else:
            min_amount, max_amount = FEE_TYPE_AMOUNT_RULES[fee_type]
            amount = Decimal(str(random.uniform(float(min_amount), float(max_amount))))

        return amount.quantize(Decimal("0.01"))

    def generate_fee_deadline(self, month_offset):
        current = timezone.localtime(timezone.now())
        month_number = current.month - 1 + month_offset
        year = current.year + month_number // 12
        month = month_number % 12 + 1
        naive_deadline = datetime(year, month, 25, 23, 59, 59)

        return timezone.make_aware(naive_deadline, timezone.get_current_timezone())

    def generate_fee_status(self, deadline):
        if deadline < timezone.now():
            return random.choice(["paid", "overdue", "unpaid"])

        return random.choice(["paid", "unpaid"])
