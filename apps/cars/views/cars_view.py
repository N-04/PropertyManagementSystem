# 文件说明：处理 apps/cars/views/cars_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.db.models import Q
from rest_framework.views import APIView

from apps.cars.serializers.cars_serializer import CarSerializer
from apps.logs.services.log_service import save_operation_log
from common.response.response import ResponseSuccess, ResponseError
from apps.cars.models import Car


class CarCreateView(APIView):
    """
    新增车辆
    """

    def post(self, request):

        plate_no = request.data.get("plate_no")

        exists = Car.objects.filter(plate_no=plate_no).exists()

        if exists:
            return ResponseError(msg="车牌号已存在")

        serializer = CarSerializer(data=request.data)

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

    def get(self, request):

        keyword = request.GET.get("keyword")
        queryset = Car.objects.all()

        if keyword:
            queryset = queryset.filter(
                Q(plate_no__icontains=keyword) | Q(owner__name__icontains=keyword)
            )

        serializer = CarSerializer(
            queryset.order_by("-id"),
            many=True,
        )

        return ResponseSuccess(data=serializer.data)


class CarUpdateView(APIView):
    """
    修改车辆
    """

    def put(self, request, pk):

        try:
            instance = Car.objects.get(pk=pk)

        except Car.DoesNotExist:
            return ResponseError(msg="车辆不存在")

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

    def delete(self, request, pk):

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

    def get(self, request, pk):

        try:
            instance = Car.objects.get(pk=pk)

        except Car.DoesNotExist:
            return ResponseError(msg="车辆不存在")

        serializer = CarSerializer(instance)

        return ResponseSuccess(data=serializer.data)


class CarDisableView(APIView):
    """
    禁用车辆
    """

    def put(self, request, pk):
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

    def put(self, request, pk):
        car = Car.objects.filter(id=pk).first()

        if not car:
            return ResponseError(msg="车辆不存在")

        # 修改车辆状态为启用
        car.status = "enabled"
        car.save()

        return ResponseSuccess(msg="启用成功")
