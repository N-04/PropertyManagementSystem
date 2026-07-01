from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.community.models import Building, Community, House, Unit
from apps.owners.models import Owner
from apps.users.models import Role, User
from apps.visitors.models import Visitor


class VisitorStatisticsPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        owner_role = Role.objects.create(name="业主", code="owner")
        repair_role = Role.objects.create(name="维修员", code="repair_staff")
        property_role = Role.objects.create(name="物业管理员", code="property_admin")

        self.owner_user = User.objects.create_user(
            username="owner_a",
            phone="18800000001",
            password="Wy@Test123",
            role=owner_role,
        )
        self.repair_user = User.objects.create_user(
            username="repair_a",
            phone="18800000003",
            password="Wy@Test123",
            role=repair_role,
        )
        self.property_user = User.objects.create_user(
            username="property_a",
            phone="18800000004",
            password="Wy@Test123",
            role=property_role,
        )

        community = Community.objects.create(name="一期社区", code="phase-one")
        building = Building.objects.create(
            community=community,
            name="1栋",
            code="phase-one-1",
        )
        unit = Unit.objects.create(
            building=building,
            name="1单元",
            code="phase-one-1-1",
        )
        owner_house = House.objects.create(unit=unit, room_no="0101")
        other_house = House.objects.create(unit=unit, room_no="0102")
        self.owner = Owner.objects.create(
            house=owner_house,
            name="业主A",
            phone="18800000001",
            id_card="110101199001010011",
        )
        other_owner = Owner.objects.create(
            house=other_house,
            name="业主B",
            phone="18800000002",
            id_card="110101199001010029",
        )

        now = timezone.now()
        Visitor.objects.create(
            name="访客A1",
            phone="13900000001",
            owner=self.owner,
            visit_time=now,
            status="waiting",
        )
        Visitor.objects.create(
            name="访客A2",
            phone="13900000002",
            owner=self.owner,
            visit_time=now,
            status="entered",
        )
        Visitor.objects.create(
            name="访客B1",
            phone="13900000003",
            owner=other_owner,
            visit_time=now,
            status="approved",
        )

    def get_statistics_as(self, user):
        self.client.force_authenticate(user=user)
        return self.client.get("/api/dashboard/statistics/")

    def test_owner_only_gets_own_visitor_statistics(self):
        response = self.get_statistics_as(self.owner_user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["total"], 2)
        self.assertEqual(response.data["data"]["waiting"], 1)
        self.assertEqual(response.data["data"]["entered"], 1)
        self.assertEqual(response.data["data"]["approved"], 0)

    def test_repair_user_gets_empty_visitor_statistics(self):
        response = self.get_statistics_as(self.repair_user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["total"], 0)
        self.assertEqual(response.data["data"]["today_count"], 0)

    def test_property_admin_can_get_global_visitor_statistics(self):
        response = self.get_statistics_as(self.property_user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["total"], 3)
        self.assertEqual(response.data["data"]["waiting"], 1)
        self.assertEqual(response.data["data"]["entered"], 1)
        self.assertEqual(response.data["data"]["approved"], 1)
