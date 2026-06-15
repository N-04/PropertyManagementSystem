# 文件说明：提供 Django 管理命令，用于维护或生成项目数据。

from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker

import random
import string
from django.utils import timezone

from apps.community.models.community import Community
from apps.community.models.building import Building
from apps.community.models.unit import Unit
from apps.community.models.house import House

from apps.owners.models.owner import Owner
from apps.parking.models.parking import Parking
from apps.cars.models import Car
from apps.visitors.models.visitor import Visitor
from apps.finance.models.fee import Fee

fake = Faker("zh_CN")


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

        for i in range(1, 6):

            community = Community.objects.create(
                name=f"演示小区{i}",
                code=f"COMM{i:03}",
                address=fake.address(),
                contact_name=fake.name(),
                contact_phone=self.generate_phone(),
            )

            self.communities.append(community)

        self.stdout.write("√ 小区完成")

        # ==========================
        # 生成楼栋
        # ==========================

        self.stdout.write("生成楼栋...")

        self.buildings = []

        for community in self.communities:

            for b in range(1, 11):

                building = Building.objects.create(
                    community=community,
                    name=f"{b}栋",
                    code=f"{community.code}-B{b:02d}",
                    floor_count=30,
                    unit_count=4,
                )

                self.buildings.append(building)

        self.stdout.write("√ 楼栋完成")

        # ==========================
        # 生成单元
        # ==========================

        self.stdout.write("生成单元...")

        self.units = []

        for building in self.buildings:

            for u in range(1, 5):

                unit = Unit.objects.create(
                    building=building,
                    name=f"{u}单元",
                    code=f"{building.code}-U{u:02d}",
                    floor_count=30,
                )

                self.units.append(unit)

        self.stdout.write("√ 单元完成")

        # ==========================
        # 生成房屋
        # ==========================

        self.stdout.write("生成房屋...")

        self.houses = []

        for unit in self.units:

            for floor in range(1, 31):

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
                                "vacant",
                                "occupied",
                                "renting",
                                "repairing",
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

        for house in self.houses:

            # 空置房大概率只有1个业主
            if house.status == "vacant":
                owner_count = 1
            else:
                owner_count = random.randint(1, 2)

            for index in range(owner_count):

                owner = Owner.objects.create(
                    house=house,
                    name=fake.name(),
                    phone=self.generate_phone(),
                    relationship=(
                        "self"
                        if index == 0
                        else random.choice(
                            [
                                "spouse",
                                "child",
                                "parent",
                                "other",
                            ]
                        )
                    ),
                    gender=random.choice(
                        [
                            "male",
                            "female",
                        ]
                    ),
                    birthday=fake.date_between(
                        start_date="-60y",
                        end_date="-18y",
                    ),
                    id_card=self.generate_id_card(),
                    is_primary=(index == 0),
                    remark="系统生成演示数据",
                )

                self.owners.append(owner)

            house.owner_count = owner_count

            if house.status == "vacant":
                house.resident_count = 0
            else:
                house.resident_count = random.randint(
                    owner_count,
                    owner_count + 3,
                )

            house.save()

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
        for owner in random.sample(self.owners, 3000):
            status = (
                random.choice(
                    [
                        "waiting",
                        "approved",
                        "rejected",
                        "entered",
                        "left",
                    ]
                ),
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
                visitor.entered_time = timezone.now()
            if visitor.status == "left":
                visitor.leave_time = timezone.now()
            visitor.save()
            self.visitors.append(visitor)

        self.stdout.write(
            self.style.SUCCESS(f"√ 访客完成，共生成 {len(self.visitors)} 人")
        )

        self.stdout.write("生成物业费...")

        self.fees = []

        months = [
            "2026_04",
            "2020-05",
            "2020-06",
        ]

        fee_type = random.choice(
            [
                "property",
                "water",
                "electric",
            ]
        )

        for house in self.houses:
            for month in months:
                if fee_type == "property":
                    amount = round(house.area * random.uniform(2.5, 4.5), 2)
                elif fee_type == "water":
                    amount = random.randint(30, 200)
                else:
                    amount = random.randint(80, 600)
                status = random.choice(
                    [
                        "paid",
                        "unpaid",
                    ]
                )

                fee = Fee.objects.create(
                    house=house,
                    amount=amount,
                    fee_type=fee_type,
                    fee_month=month,
                    status=status,
                    pay_time=(timezone.now() if status == "paid" else None),
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
    def generate_id_card(self):

        while True:

            card = (
                "110101"
                + str(random.randint(1965, 2005))
                + f"{random.randint(1,12):02d}"
                + f"{random.randint(1,28):02d}"
                + f"{random.randint(100,999):03d}"
                + random.choice("0123456789X")
            )

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


data = {
    "community_count": Community.objects.count(),
    "building_count": Building.objects.count(),
    "house_count": House.objects.count(),
    "owner_count": Owner.objects.count(),
    "car_count": Car.objects.count(),
    "visitor_count": Visitor.objects.count(),
    "unpaid_fee_count": Fee.objects.filter(status="unpaid").count(),
}
