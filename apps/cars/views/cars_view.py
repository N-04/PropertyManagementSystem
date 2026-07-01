# 文件说明：处理 apps/cars/views/cars_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.cars.models import Car
from apps.cars.serializers.cars_serializer import CarSerializer
from apps.logs.services.log_service import save_operation_log
from apps.owners.models import Owner
from apps.users.utils.role_access import is_owner_user, is_property_manager_user
from common.pagination.base_pagination import build_paginated_data, paginate_queryset
from common.response.response import ResponseError, ResponseSuccess


# 车辆权限分块：业主端按手机号隔离车辆，物业端保留全量管理视角。
def _owner_for_user(user):
    """根据登录手机号找到对应业主档案，用于业主侧车辆数据隔离。"""

    phone = getattr(user, "phone", None)

    if not phone:
        return None

    return Owner.objects.filter(phone=phone).first()


def _car_queryset_for_user(user):
    """按角色返回车辆可见范围，避免业主看到其他住户车辆。"""

    if is_property_manager_user(user):
        return Car.objects.all()

    if is_owner_user(user):
        owner = _owner_for_user(user)

        if owner:
            return Car.objects.filter(owner=owner)

    return Car.objects.none()


def _can_manage_cars(user):
    """车辆资料维护只开放给物业管理员，业主仅能新增和查看自己的车辆。"""

    return is_property_manager_user(user)


class CarCreateView(APIView):
    """
    新增车辆
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not (_can_manage_cars(request.user) or is_owner_user(request.user)):
            return ResponseError(msg="无权新增车辆")

        plate_no = request.data.get("plate_no")

        exists = Car.objects.filter(plate_no=plate_no).exists()

        if exists:
            return ResponseError(msg="车牌号已存在")

        data = request.data.copy()

        if not _can_manage_cars(request.user):
            owner = _owner_for_user(request.user)

            if not owner:
                return ResponseError(msg="未找到当前业主档案")

            # 业主端新增车辆只能绑定自己的业主档案，避免提交他人 owner_id。
            data["owner"] = owner.id

        serializer = CarSerializer(data=data)

        if serializer.is_valid():

            car = serializer.save()

            # 保存操作日志
            save_operation_log(
                username=request.user.username,
                module="车辆管理",
                action=f"新增车辆：{car.plate_no}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="新增成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class CarListView(APIView):
    """
    车辆列表
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        keyword = request.GET.get("keyword")
        # 列表入口先按角色裁剪，再叠加搜索和分页，避免搜索绕过数据权限。
        queryset = _car_queryset_for_user(request.user)

        if keyword:
            queryset = queryset.filter(
                Q(plate_no__icontains=keyword) | Q(owner__name__icontains=keyword)
            )

        page_queryset, page_meta = paginate_queryset(queryset.order_by("-id"), request)
        serializer = CarSerializer(page_queryset, many=True)

        return ResponseSuccess(data=build_paginated_data(serializer.data, page_meta))


class CarUpdateView(APIView):
    """
    修改车辆
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not _can_manage_cars(request.user):
            return ResponseError(msg="无权修改车辆")

        try:
            instance = Car.objects.get(pk=pk)

        except Car.DoesNotExist:
            return ResponseError(msg="车辆不存在")

        # 管理员编辑车辆时允许局部更新，前端详情页不会因为缺少非必填字段失败。
        serializer = CarSerializer(
            instance,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            serializer.save()

            save_operation_log(
                username=request.user.username,
                module="车辆管理",
                action=f"修改车辆：{instance.plate_no}",
            )

            return ResponseSuccess(
                data=serializer.data,
                msg="修改成功",
            )

        return ResponseError(
            msg="参数错误",
            data=serializer.errors,
        )


class CarDeleteView(APIView):
    """
    删除车辆
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not _can_manage_cars(request.user):
            return ResponseError(msg="无权删除车辆")

        # 查询车辆
        instance = Car.objects.filter(id=pk).first()

        # 不存在
        if not instance:
            return ResponseError(msg="车辆不存在")

        # 保存操作日志
        save_operation_log(
            username=request.user.username,
            module="车辆管理",
            action=f"删除车辆：{instance.plate_no}",
        )

        # 删除车辆
        instance.delete()

        return ResponseSuccess(msg="删除成功")


class CarDetailView(APIView):
    """
    车辆详情
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        instance = _car_queryset_for_user(request.user).filter(pk=pk).first()

        if not instance:
            return ResponseError(msg="车辆不存在")

        serializer = CarSerializer(instance)

        return ResponseSuccess(data=serializer.data)


class CarDisableView(APIView):
    """
    禁用车辆
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not _can_manage_cars(request.user):
            return ResponseError(msg="无权禁用车辆")

        # 根据主键查询车辆
        car = Car.objects.filter(id=pk).first()

        # 判断车辆是否存在
        if not car:
            return ResponseError(msg="车辆不存在")

        # 修改车辆状态为禁用
        car.status = "disabled"
        car.save()

        # 返回成功结果
        return ResponseSuccess(msg="禁用成功")


class CarEnableView(APIView):
    """
    启用车辆
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not _can_manage_cars(request.user):
            return ResponseError(msg="无权启用车辆")

        car = Car.objects.filter(id=pk).first()

        if not car:
            return ResponseError(msg="车辆不存在")

        # 修改车辆状态为启用
        car.status = "normal"
        car.save()

        return ResponseSuccess(msg="启用成功")
